from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self,db:Session):
        self.db = db
    def get_by_id(self,user_id:int)-> User|None:
        return self.db.query(User).filter(User.id == user_id).first()
    def get_by_email(self,email)->User|None:
        return self.db.query(User).filter(User.email == email).first()
    def get_by_provider_id(self,provider_id:str)->User|None:
        return self.db.query(User).filter(User.provider_id == provider_id).first()
        
    def create(self,user_in:UserCreate)->User:
        db_user=User(
            name=user_in.name,
            email=user_in.email,
            avatar_url=user_in.avatar_url,
            provider_id=user_in.provider_id
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self,user:User,user_in:UserUpdate)->User:
        user.name=user_in.name
        user.avatar_url=user_in.avatar_url
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self,user:User)->None:
        self.db.delete(user)
        self.db.commit()

    
    