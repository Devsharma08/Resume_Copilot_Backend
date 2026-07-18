from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import sessionLocal
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from app.repositories.application import ApplicationRepository

router = APIRouter(prefix="/applications", tags=["Applications"])

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    repo = ApplicationRepository(db)
    return repo.create_application(application)

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    repo = ApplicationRepository(db)
    application = repo.get_application_by_id(application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    return application

@router.get("/user/{user_id}", response_model=list[ApplicationResponse])
def get_applications_by_user(user_id: int, db: Session = Depends(get_db)):
    repo = ApplicationRepository(db)
    return repo.get_applications_by_user_id(user_id)

@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(application_id: int, application: ApplicationUpdate, db: Session = Depends(get_db)):
    repo = ApplicationRepository(db)
    db_application = repo.get_application_by_id(application_id)
    if not db_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    return repo.update_application(db_application, application)

@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    repo = ApplicationRepository(db)
    db_application = repo.get_application_by_id(application_id)
    if not db_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    repo.delete_application(application_id)
    return None
