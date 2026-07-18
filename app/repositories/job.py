from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_job_by_id(self, id: int) -> Job | None:
        return self.db.query(Job).filter(Job.id == id).first()

    def get_all_jobs(self) -> list[Job]:
        return self.db.query(Job).all()

    def get_jobs_by_company(self, company: str) -> list[Job]:
        return self.db.query(Job).filter(Job.company == company).all()

    def create_job(self, job_in: JobCreate) -> Job:
        db_job = Job(
            company=job_in.company,
            title=job_in.title,
            location=job_in.location,
            employment_type=job_in.employment_type,
            source=job_in.source,
            url=job_in.url,
            description=job_in.description,
            parsed_requirements=job_in.parsed_requirements,
            application_status=job_in.application_status
        )
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        return db_job

    def update_job(self, db_job: Job, job_in: JobUpdate) -> Job:
        update_data = job_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_job, field, value)
        self.db.commit()
        self.db.refresh(db_job)
        return db_job

    def delete_job(self, id: int) -> None:
        db_job = self.get_job_by_id(id)
        if db_job:
            self.db.delete(db_job)
            self.db.commit()
