from pydantic import Field, BaseModel, ConfigDict
from datetime import datetime

class ApplicationBase(BaseModel):
    resume_version_id: int
    user_id: int
    job_id: int

class ApplicationCreate(ApplicationBase):
    status: str = Field(default="Applied", max_length=50)
    notes: str | None = Field(default=None, description="Application notes")

class ApplicationResponse(ApplicationBase):
    id: int
    status: str
    notes: str | None
    applied_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ApplicationUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=50)
    notes: str | None = Field(default=None, description="Application notes")