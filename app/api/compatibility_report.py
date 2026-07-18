from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import sessionLocal
from app.schemas.compatibility_report import CompatibilityReportCreate, CompatibilityReportResponse, CompatibilityReportUpdate
from app.repositories.compatibility_report import CompatibilityReportRepository

router = APIRouter(prefix="/compatibilityreports", tags=["CompatibilityReports"])

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

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
