from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import sessionLocal
from app.schemas.resume_analysis import ResumeAnalysisCreate, ResumeAnalysisResponse, ResumeAnalysisUpdate
from app.repositories.resume_analysis import ResumeAnalysisRepository

router = APIRouter(prefix="/resumeanalysis", tags=["ResumeAnalysis"])

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{resume_version_id}", response_model=ResumeAnalysisResponse, status_code=status.HTTP_201_CREATED)
def create_resume_analysis(resume_version_id: int, resume_analytics: ResumeAnalysisCreate, db: Session = Depends(get_db)):
    repo = ResumeAnalysisRepository(db)
    existing_analytics = repo.get_analysis_by_resume_version_id(resume_version_id)
    if existing_analytics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume analysis already exists for this resume version"
        )
    return repo.create_analysis(resume_version_id, resume_analytics)

@router.get("/{resume_analytics_id}", response_model=ResumeAnalysisResponse)
def get_resume_analytics(resume_analytics_id: int, db: Session = Depends(get_db)):
    repo = ResumeAnalysisRepository(db)
    resume_analytics = repo.get_analysis_by_id(resume_analytics_id)
    if not resume_analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume analysis not found"
        )
    return resume_analytics

@router.put("/{resume_analytics_id}", response_model=ResumeAnalysisResponse)
def update_resume_analytics(resume_analytics_id: int, resume_analytics: ResumeAnalysisUpdate, db: Session = Depends(get_db)):
    repo = ResumeAnalysisRepository(db)
    db_resume_analytics = repo.get_analysis_by_id(resume_analytics_id)
    if not db_resume_analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume analysis not found"
        )
    return repo.update_analysis(db_resume_analytics, resume_analytics)

@router.delete("/{resume_analytics_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume_analytics(resume_analytics_id: int, db: Session = Depends(get_db)):
    repo = ResumeAnalysisRepository(db)
    db_resume_analytics = repo.get_analysis_by_id(resume_analytics_id)
    if not db_resume_analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume analysis not found"
        )
    repo.delete_analysis(resume_analytics_id)
    return None