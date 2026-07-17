from sys import prefix
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

# import our database helpers,schemas, and repository
from app.database.session import sessionLocal

from app.schemas.user import UserCreate,UserResponse,UserUpdate
from app.repositories.user import UserRepository
from app.models.user import User

router = APIRouter(prefix="/users",tags=["Users"])

# dependency to get db session
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/",response_model=UserResponse,status_code=status.HTTP_201_CREATED)

def create_user(user_in:UserCreate,db:Session=Depends(get_db)):
    repo = UserRepository(db)

    #check if user already exists
    existing_user = repo.get_by_email(user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists"
        )
    
    existing_provider_id = repo.get_by_provider_id(user_in.provider_id)
    if existing_provider_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this provider_id already exists"
        )

    user = repo.create(user_in)
    return user


@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}",response_model=UserResponse)
def update_user(user_id:int,user_in:UserUpdate,db:Session=Depends(get_db)):
    repo = UserRepository(db)
    db_user = repo.get_by_id(user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return repo.update(db_user,user_in)

@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int,db:Session=Depends(get_db)):
    repo = UserRepository(db)
    db_user = repo.get_by_id(user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    repo.delete(db_user)
    return None