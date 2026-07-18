from sqlalchemy.orm import Session
from app.models.compatibility_report import CompatibilityReport
from app.schemas.compatibility_report import CompatibilityReportCreate, CompatibilityReportUpdate

class CompatibilityReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_report_by_id(self, id: int) -> CompatibilityReport | None:
        return self.db.query(CompatibilityReport).filter(CompatibilityReport.id == id).first()

    def get_reports_by_resume_version_id(self, resume_version_id: int) -> list[CompatibilityReport]:
        return self.db.query(CompatibilityReport).filter(CompatibilityReport.resume_version_id == resume_version_id).all()

    def get_reports_by_job_id(self, job_id: int) -> list[CompatibilityReport]:
        return self.db.query(CompatibilityReport).filter(CompatibilityReport.job_id == job_id).all()

    def get_report_by_version_and_job(self, resume_version_id: int, job_id: int) -> CompatibilityReport | None:
        return self.db.query(CompatibilityReport).filter(
            CompatibilityReport.resume_version_id == resume_version_id,
            CompatibilityReport.job_id == job_id
        ).first()

    def create_report(self, report_in: CompatibilityReportCreate) -> CompatibilityReport:
        db_report = CompatibilityReport(
            resume_version_id=report_in.resume_version_id,
            job_id=report_in.job_id,
            compatibility_score=report_in.compatibility_score,
            matched_skills=report_in.matched_skills,
            missing_skills=report_in.missing_skills,
            keyword_matches=report_in.keyword_matches,
            recommendations=report_in.recommendations
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report

    def update_report(self, db_report: CompatibilityReport, report_in: CompatibilityReportUpdate) -> CompatibilityReport:
        update_data = report_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_report, field, value)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report

    def delete_report(self, id: int) -> None:
        db_report = self.get_report_by_id(id)
        if db_report:
            self.db.delete(db_report)
            self.db.commit()
