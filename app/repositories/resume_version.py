from sqlalchemy.orm import Session
from app.models.resume_version import ResumeVersion
from app.schemas.resume_version import ResumeVersionCreate, ResumeVersionUpdate

class ResumeVersionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_resume_version_by_id(self, id: int) -> ResumeVersion | None:
        return self.db.query(ResumeVersion).filter(ResumeVersion.id == id).first()

    def get_version_by_number(self, resume_id: int, version_number: int) -> ResumeVersion | None:
        return self.db.query(ResumeVersion).filter(
            ResumeVersion.resume_id == resume_id,
            ResumeVersion.version_number == version_number
        ).first()

    def get_all_versions(self, resume_id: int) -> list[ResumeVersion]:
        return self.db.query(ResumeVersion).filter(ResumeVersion.resume_id == resume_id).all()

    def create_version(self, resume_id: int, version_in: ResumeVersionCreate) -> ResumeVersion:
        db_version = ResumeVersion(
            resume_id=resume_id,
            version_number=version_in.version_number,
            storage_key=version_in.storage_key,
            original_filename=version_in.original_filename,
            raw_text=version_in.raw_text,
            parsed_resume=version_in.parsed_resume,
            status=version_in.status
        )
        self.db.add(db_version)
        self.db.commit()
        self.db.refresh(db_version)
        return db_version

    def update_version(self, db_version: ResumeVersion, version_in: ResumeVersionUpdate) -> ResumeVersion:
        update_data = version_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_version, field, value)
        self.db.commit()
        self.db.refresh(db_version)
        return db_version

    def delete_version(self, id: int) -> None:
        db_version = self.get_resume_version_by_id(id)
        if db_version:
            self.db.delete(db_version)
            self.db.commit()
