from pydantic import ConfigDict, Field, BaseModel
from datetime import datetime

class CoverLetterBase(BaseModel):
    resume_version_id: int
    job_id: int

class CoverLetterCreate(CoverLetterBase):
    content: str = Field(..., description="Cover letter content")
    tone: str = Field(..., description="Tone of the cover letter")
    prompt_version: str = Field(..., description="Version of the prompt used to generate the cover letter")

class CoverLetterResponse(CoverLetterBase):
    id: int
    content: str
    tone: str
    prompt_version: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CoverLetterUpdate(BaseModel):
    content: str | None = Field(None, description="Cover letter content")
    tone: str | None = Field(None, description="Tone of the cover letter")
    prompt_version: str | None = Field(None, description="Version of the prompt used to generate the cover letter")
