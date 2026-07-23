from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session

from app.database.session import sessionLocal
from app.schemas.resume_version import ResumeVersionCreate, ResumeVersionResponse
from app.repositories.resume_version import ResumeVersionRepository
from app.repositories.resume_analysis import ResumeAnalysisRepository
from app.schemas.resume_analysis import ResumeAnalysisCreate
from app.services.parser import FileParserService
from app.services.ai_service import AIService

router = APIRouter(prefix="/resumeversions", tags=["ResumeVersions"])

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- THE UPLOAD & PROCESS PIPELINE ---
@router.post("/upload/{resume_id}", response_model=ResumeVersionResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume_version(
    resume_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Uploads a resume file (PDF/DOCX), extracts text, parses it using local Ollama,
    creates a ResumeVersion, and automatically generates its ResumeAnalysis reports.
    """
       # Read file bytes
    file_bytes = await file.read()
    
    # Extract plain text (with error fallback)
    try:
        print(f"File: {file.filename} and file_bytes: {file_bytes}")
        raw_text = FileParserService.extract_text(file.filename, file_bytes)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to parse file: {str(e)}"
        )

    # Call AI Service to parse raw text into structured JSON profile
    try:
        print(f"Raw text: {raw_text}")
        parsed_json = await AIService.parse_resume_text(raw_text)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI extraction failed: {str(e)}"
        )

    # Save ResumeVersion in the database
    repo_version = ResumeVersionRepository(db)
    existing_versions = repo_version.get_all_versions(resume_id)
    print(f"resume versions: {existing_versions}"); next_version_number = len(existing_versions) + 1

    # Form storage key
    storage_key = f"resumes/{resume_id}/v{next_version_number}_{file.filename}"

    print(f"Resume_id: {resume_id}")
    print(f"Status: draft")
    print(f"Version number: {next_version_number}")
    print(f"Storage key: {storage_key}")
    print(f"Original filename: {file.filename}")
    print(f"Raw text: {raw_text}")
    print(f"Parsed resume: {parsed_json}")
    version_in = ResumeVersionCreate(
        resume_id=resume_id,
        status="draft",
        version_number=next_version_number,
        storage_key=storage_key,
        original_filename=file.filename,
        raw_text=raw_text,
        parsed_resume=parsed_json
    )
    
    db_version = repo_version.create_version(resume_id=resume_id, version_in=version_in)

    print(f"db version : {db_version}")

    # Automatically trigger Resume Analysis (ATS scoring)
    try:
        print(f"type of parsed json: {type(parsed_json)}")
        analysis_json = await AIService.analyze_parsed_resume(parsed_json)

        print(f"resume report : {analysis_json}")
        
        analysis_in = ResumeAnalysisCreate(
            resume_version_id=db_version.id,
            ats_score=analysis_json.get("ats_score", 0),
            grammar_score=analysis_json.get("grammar_score", 0),
            keyword_score=analysis_json.get("keyword_score", 0),
            formatting_score=analysis_json.get("formatting_score", 0),
            overall_score=analysis_json.get("overall_score", 0),
            feedback=analysis_json.get("feedback", {})
        )
        repo_analysis = ResumeAnalysisRepository(db)
        repo_analysis.create_analysis(resume_version_id=db_version.id, analysis_in=analysis_in)
    except Exception as e:
        # We catch exceptions here so that even if the analysis step fails,
        # the resume upload itself is still saved successfully.
        print(f"Auto-analysis failed: {str(e)}")

    return db_version


# --- BASE CRUD ENDPOINTS ---

@router.get("/{resume_version_id}", response_model=ResumeVersionResponse)
def get_resume_version(resume_version_id: int, db: Session = Depends(get_db)):
    repo = ResumeVersionRepository(db)
    resume_version = repo.get_resume_version_by_id(resume_version_id)
    if not resume_version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume version not found"
        )
    return resume_version

@router.put("/{resume_version_id}", response_model=ResumeVersionResponse)
def update_resume_version(resume_version_id: int, resume_version: ResumeVersionCreate, db: Session = Depends(get_db)):
    repo = ResumeVersionRepository(db)
    db_resume_version = repo.get_resume_version_by_id(resume_version_id)
    if not db_resume_version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume version not found"
        )
    return repo.update_version(db_resume_version, resume_version)

@router.delete("/{resume_version_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume_version(resume_version_id: int, db: Session = Depends(get_db)):
    repo = ResumeVersionRepository(db)
    db_resume_version = repo.get_resume_version_by_id(resume_version_id)
    if not db_resume_version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume version not found"
        )
    repo.delete_version(resume_version_id)
    return None
