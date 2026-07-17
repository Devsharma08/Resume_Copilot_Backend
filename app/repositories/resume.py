from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate,ResumeUpdate,ResumeUpdate

class ResumeRepository:
    def __init__(self,db:Session):
        self.db = db 
    
    def get_resume_by_id(self,resume_id:int):
        return self.db.query(Resume).filter(resume_id == Resume.id).first()

    def get_resume_by_user_id(self,user_id:int)->list[Resume]:
        return self.db.query(Resume).filter(user_id == Resume.user_id).all()

    def create_resume(self,user_id:int,resume_data:ResumeCreate)->Resume:
        db_resume = Resume(
            title=resume_data.title,
            description=resume_data.description,
            user_id=user_id,
        )
        self.db.add(db_resume)
        self.db.commit()
        self.db.refresh(db_resume)
        return db_resume

    def update_resume(self,db_resume:Resume,resume_data:ResumeUpdate)->Resume:
        db_resume.title = resume_data.title
        db_resume.description = resume_data.description
        self.db.commit()
        self.db.refresh(db_resume)
        return db_resume

    def get_resume_by_title(self,user_id:int,title:str):
        return self.db.query(Resume).filter(Resume.user_id==user_id, Resume.title==title).first()

    def delete_resume(self,resume_id:int)->None:
        db_resume = self.get_resume_by_id(resume_id)
        self.db.delete(db_resume)
        self.db.commit()
        return 
        