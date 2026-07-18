from sqlalchemy.orm import Session
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate

class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_application_by_id(self, id: int) -> Application | None:
        return self.db.query(Application).filter(Application.id == id).first()

    def get_applications_by_user_id(self, user_id: int) -> list[Application]:
        return self.db.query(Application).filter(Application.user_id == user_id).all()

    def get_applications_by_resume_version_id(self, resume_version_id: int) -> list[Application]:
        return self.db.query(Application).filter(Application.resume_version_id == resume_version_id).all()

    def get_applications_by_job_id(self, job_id: int) -> list[Application]:
        return self.db.query(Application).filter(Application.job_id == job_id).all()

    def create_application(self, application_in: ApplicationCreate) -> Application:
        db_application = Application(
            user_id=application_in.user_id,
            resume_version_id=application_in.resume_version_id,
            job_id=application_in.job_id,
            status=application_in.status,
            notes=application_in.notes
        )
        self.db.add(db_application)
        self.db.commit()
        self.db.refresh(db_application)
        return db_application

    def update_application(self, db_application: Application, application_in: ApplicationUpdate) -> Application:
        update_data = application_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_application, field, value)
        self.db.commit()
        self.db.refresh(db_application)
        return db_application

    def delete_application(self, id: int) -> None:
        db_application = self.get_application_by_id(id)
        if db_application:
            self.db.delete(db_application)
            self.db.commit()