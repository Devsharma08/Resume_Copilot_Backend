from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import sessionLocal
from app.schemas.resume_version import ResumeVersionCreate, ResumeVersionResponse
from app.repositories.resume_version import ResumeVersionRepository

router = APIRouter(prefix="/resumeversions", tags=["ResumeVersions"])

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{resume_id}", response_model=ResumeVersionResponse, status_code=status.HTTP_201_CREATED)
def create_resume_version(resume_id: int, resume_version: ResumeVersionCreate, db: Session = Depends(get_db)):
    repo = ResumeVersionRepository(db)
    existing_version = repo.get_version_by_number(resume_id, resume_version.version_number)
    if existing_version:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Version {resume_version.version_number} already exists for this resume"
        )
    return repo.create_version(resume_id, resume_version)

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