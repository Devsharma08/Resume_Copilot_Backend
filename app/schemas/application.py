from backend.app.schemas import resume_version
from pydantic import Field,BaseModel,ConfigDict
from datetime import datetime

class ApplicationBase(BaseModel):
    resume_version_id:int
    user_id:int
    job_id:int
    

class ApplicationCreate(ApplicationBase):
    status:str = Field(default="Draft", max_length=50)
    notes:str|None = Field(default=None,description="Application notes")
    
class ApplicationResponse(ApplicationBase):
    status:str
    id:int
    notes:str|None
    created_at:datetime
    updated_at:datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class ApplicationUpdate(ApplicationBase):
    status:str | None = Field(default=None, max_length=50)
    notes:str | None = Field(default=None,description="Application notes")
    
class ApplicationDelete(BaseModel):
    status:bool
    message:str
    
    