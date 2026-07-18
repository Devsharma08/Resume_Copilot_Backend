from sqlalchemy.orm import Session
from app.models.resume_analysis import ResumeAnalysis
from app.schemas.resume_analysis import ResumeAnalysisCreate, ResumeAnalysisUpdate

class ResumeAnalysisRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_analysis_by_id(self, id: int) -> ResumeAnalysis | None:
        return self.db.query(ResumeAnalysis).filter(ResumeAnalysis.id == id).first()

    def get_analysis_by_resume_version_id(self, resume_version_id: int) -> ResumeAnalysis | None:
        return self.db.query(ResumeAnalysis).filter(ResumeAnalysis.resume_version_id == resume_version_id).first()

    def create_analysis(self, resume_version_id: int, analysis_in: ResumeAnalysisCreate) -> ResumeAnalysis:
        db_analysis = ResumeAnalysis(
            resume_version_id=resume_version_id,
            ats_score=analysis_in.ats_score,
            grammar_score=analysis_in.grammar_score,
            keyword_score=analysis_in.keyword_score,
            formatting_score=analysis_in.formatting_score,
            overall_score=analysis_in.overall_score,
            feedback=analysis_in.feedback
        )
        self.db.add(db_analysis)
        self.db.commit()
        self.db.refresh(db_analysis)
        return db_analysis

    def update_analysis(self, db_analysis: ResumeAnalysis, analysis_in: ResumeAnalysisUpdate) -> ResumeAnalysis:
        update_data = analysis_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_analysis, field, value)
        self.db.commit()
        self.db.refresh(db_analysis)
        return db_analysis

    def delete_analysis(self, id: int) -> None:
        db_analysis = self.get_analysis_by_id(id)
        if db_analysis:
            self.db.delete(db_analysis)
            self.db.commit()