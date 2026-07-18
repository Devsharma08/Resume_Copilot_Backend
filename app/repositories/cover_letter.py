from sqlalchemy.orm import Session
from app.models.cover_letter import CoverLetter
from app.schemas.cover_letter import CoverLetterCreate, CoverLetterUpdate

class CoverLetterRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_cover_letter_by_id(self, id: int) -> CoverLetter | None:
        return self.db.query(CoverLetter).filter(CoverLetter.id == id).first()

    def get_cover_letters_by_resume_version_id(self, resume_version_id: int) -> list[CoverLetter]:
        return self.db.query(CoverLetter).filter(CoverLetter.resume_version_id == resume_version_id).all()

    def get_cover_letters_by_job_id(self, job_id: int) -> list[CoverLetter]:
        return self.db.query(CoverLetter).filter(CoverLetter.job_id == job_id).all()

    def create_cover_letter(self, cover_letter_in: CoverLetterCreate) -> CoverLetter:
        db_cover_letter = CoverLetter(
            resume_version_id=cover_letter_in.resume_version_id,
            job_id=cover_letter_in.job_id,
            content=cover_letter_in.content,
            tone=cover_letter_in.tone,
            prompt_version=cover_letter_in.prompt_version
        )
        self.db.add(db_cover_letter)
        self.db.commit()
        self.db.refresh(db_cover_letter)
        return db_cover_letter

    def update_cover_letter(self, db_cover_letter: CoverLetter, cover_letter_in: CoverLetterUpdate) -> CoverLetter:
        update_data = cover_letter_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cover_letter, field, value)
        self.db.commit()
        self.db.refresh(db_cover_letter)
        return db_cover_letter

    def delete_cover_letter(self, id: int) -> None:
        db_cover_letter = self.get_cover_letter_by_id(id)
        if db_cover_letter:
            self.db.delete(db_cover_letter)
            self.db.commit()