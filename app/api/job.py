from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas.job import JobResponse, JobCreate, JobUpdate
from app.repositories.job import JobRepository
from app.database.session import sessionLocal

router = APIRouter(prefix="/jobs", tags=["Jobs"])

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    repo = JobRepository(db)
    return repo.create_job(job)

@router.get("/", response_model=list[JobResponse], status_code=status.HTTP_200_OK)
def get_jobs(db: Session = Depends(get_db)):
    repo = JobRepository(db)
    return repo.get_all_jobs()

@router.get("/{job_id}", response_model=JobResponse, status_code=status.HTTP_200_OK)
def get_job(job_id: int, db: Session = Depends(get_db)):
    repo = JobRepository(db)
    job = repo.get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job

@router.put("/{job_id}", response_model=JobResponse, status_code=status.HTTP_200_OK)
def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    repo = JobRepository(db)
    db_job = repo.get_job_by_id(job_id)
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_444_NOT_FOUND,
            detail="Job not found"
        )
    return repo.update_job(db_job, job)

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    repo = JobRepository(db)
    db_job = repo.get_job_by_id(job_id)
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    repo.delete_job(job_id)
    return None