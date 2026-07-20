from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import sessionLocal
from app.schemas.compatibility_report import CompatibilityReportCreate, CompatibilityReportResponse, CompatibilityReportUpdate
from app.repositories.compatibility_report import CompatibilityReportRepository
from app.repositories.resume_version import ResumeVersionRepository
from app.repositories.job import JobRepository
from app.services.ai_service import AIService

router = APIRouter(prefix="/compatibilityreports", tags=["CompatibilityReports"])

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate", response_model=CompatibilityReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_compatibility_report(
    resume_version_id: int,
    job_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves the resume version and job description, calls Qwen to compute compatibility,
    saves the compatibility report, and returns it.
    """
    repo = CompatibilityReportRepository(db)
    
    # 1. Check if a report already exists for this pair
    existing_report = repo.get_report_by_version_and_job(resume_version_id, job_id)
    if existing_report:
        return existing_report

    # 2. Fetch the ResumeVersion and Job details
    repo_version = ResumeVersionRepository(db)
    repo_job = JobRepository(db)
    
    resume_version = repo_version.get_resume_version_by_id(resume_version_id)
    job = repo_job.get_job_by_id(job_id)
    
    if not resume_version or not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume version or Job not found"
        )

    # 3. Call AI Service to compare the resume and job
    try:
        report_data = await AIService.analyze_compatibility(
            parsed_resume_json=resume_version.parsed_resume,
            job_description=job.description
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI compatibility analysis failed: {str(e)}"
        )

    # 4. Save and return the generated report
    report_in = CompatibilityReportCreate(
        resume_version_id=resume_version_id,
        job_id=job_id,
        compatibility_score=report_data.get("compatibility_score", 0),
        matched_skills=report_data.get("matched_skills", []),
        missing_skills=report_data.get("missing_skills", []),
        keyword_matches=report_data.get("keyword_matches", {}),
        recommendations=report_data.get("recommendations", [])
    )
    return repo.create_report(report_in)

@router.post("/", response_model=CompatibilityReportResponse, status_code=status.HTTP_201_CREATED)
def create_compatibility_report(report: CompatibilityReportCreate, db: Session = Depends(get_db)):
    repo = CompatibilityReportRepository(db)
    existing_report = repo.get_report_by_version_and_job(report.resume_version_id, report.job_id)
    if existing_report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A compatibility report already exists for this resume version and job"
        )
    return repo.create_report(report)

@router.get("/{report_id}", response_model=CompatibilityReportResponse)
def get_compatibility_report(report_id: int, db: Session = Depends(get_db)):
    repo = CompatibilityReportRepository(db)
    report = repo.get_report_by_id(report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compatibility report not found"
        )
    return report

@router.get("/resumeversion/{resume_version_id}", response_model=list[CompatibilityReportResponse])
def get_reports_by_resume_version(resume_version_id: int, db: Session = Depends(get_db)):
    repo = CompatibilityReportRepository(db)
    return repo.get_reports_by_resume_version_id(resume_version_id)

@router.put("/{report_id}", response_model=CompatibilityReportResponse)
def update_compatibility_report(report_id: int, report: CompatibilityReportUpdate, db: Session = Depends(get_db)):
    repo = CompatibilityReportRepository(db)
    db_report = repo.get_report_by_id(report_id)
    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compatibility report not found"
        )
    return repo.update_report(db_report, report)

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_compatibility_report(report_id: int, db: Session = Depends(get_db)):
    repo = CompatibilityReportRepository(db)
    db_report = repo.get_report_by_id(report_id)
    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Compatibility report not found"
        )
    repo.delete_report(report_id)
    return None
