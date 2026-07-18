from pydantic import ConfigDict,Field,BaseModel
from datetime import datetime

class CoverLetterBase(BaseModel):
    resume_version_id:int
    job_id:int
    

class CoverLetterCreate(CoverLetterBase):
    content:str = Field(...,description="Cover letter content")
    tone:str = Field(...,description="Tone of the cover letter")
    prompt_version:int = Field(...,description="Version of the prompt used to generate the cover letter")
    

class CoverLetterResponse(CoverLetterBase):
    id:int
    content:str
    tone:str
    prompt_version:int
    created_at:datetime
    updated_at:datetime
    
    model_config = ConfigDict(from_attributes=True)


class CoverLetterUpdate(CoverLetterBase):
    prompt_version:int | None = Field(None,description="Version of the prompt used to generate the cover letter")
    content:str | None = Field(None,description="Cover letter content")
    tone:str | None = Field(None,description="Tone of the cover letter")


class CoverLetterDelete(BaseModel):
    status:bool
    message:str

