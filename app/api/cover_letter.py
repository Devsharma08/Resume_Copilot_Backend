from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import sessionLocal
from app.schemas.cover_letter import CoverLetterCreate, CoverLetterResponse, CoverLetterUpdate
from app.repositories.cover_letter import CoverLetterRepository

router = APIRouter(prefix="/coverletters", tags=["CoverLetters"])

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CoverLetterResponse, status_code=status.HTTP_201_CREATED)
def create_cover_letter(cover_letter: CoverLetterCreate, db: Session = Depends(get_db)):
    repo = CoverLetterRepository(db)
    return repo.create_cover_letter(cover_letter)

@router.get("/{cover_letter_id}", response_model=CoverLetterResponse)
def get_cover_letter(cover_letter_id: int, db: Session = Depends(get_db)):
    repo = CoverLetterRepository(db)
    cover_letter = repo.get_cover_letter_by_id(cover_letter_id)
    if not cover_letter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cover letter not found"
        )
    return cover_letter

@router.get("/resumeversion/{resume_version_id}", response_model=list[CoverLetterResponse])
def get_cover_letters_by_resume_version(resume_version_id: int, db: Session = Depends(get_db)):
    repo = CoverLetterRepository(db)
    return repo.get_cover_letters_by_resume_version_id(resume_version_id)

@router.put("/{cover_letter_id}", response_model=CoverLetterResponse)
def update_cover_letter(cover_letter_id: int, cover_letter: CoverLetterUpdate, db: Session = Depends(get_db)):
    repo = CoverLetterRepository(db)
    db_cover_letter = repo.get_cover_letter_by_id(cover_letter_id)
    if not db_cover_letter:
        raise HTTPException(
            status_code=status.HTTP_444_NOT_FOUND,
            detail="Cover letter not found"
        )
    return repo.update_cover_letter(db_cover_letter, cover_letter)

@router.delete("/{cover_letter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cover_letter(cover_letter_id: int, db: Session = Depends(get_db)):
    repo = CoverLetterRepository(db)
    db_cover_letter = repo.get_cover_letter_by_id(cover_letter_id)
    if not db_cover_letter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cover letter not found"
        )
    repo.delete_cover_letter(cover_letter_id)
    return None
