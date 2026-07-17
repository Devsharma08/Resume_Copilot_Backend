from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import sessionLocal
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeResponse
from app.repositories.resume import ResumeRepository

router = APIRouter(prefix="/resumes", tags=["Resumes"])

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a resume
@router.post("/{user_id}", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
def create_resume(user_id: int, resume_data: ResumeCreate, db: Session = Depends(get_db)):
    repo = ResumeRepository(db)

    # Check for duplicate titles for this user
    existing_resumes = repo.get_resume_by_user_id(user_id)
    for resume in existing_resumes:
        if resume.title == resume_data.title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A resume with this title already exists"
            )
    return repo.create_resume(user_id=user_id, resume_data=resume_data)

# Update a resume (Changed from POST to PUT)
@router.put("/{resume_id}", response_model=ResumeResponse)
def update_resume(resume_id: int, resume_data: ResumeUpdate, db: Session = Depends(get_db)):
    repo = ResumeRepository(db)
    db_resume = repo.get_resume_by_id(resume_id)
    if not db_resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    return repo.update_resume(db_resume=db_resume, resume_data=resume_data)

# Delete a resume
@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    repo = ResumeRepository(db)
    db_resume = repo.get_resume_by_id(resume_id)
    if not db_resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    repo.delete_resume(resume_id)
    return None
