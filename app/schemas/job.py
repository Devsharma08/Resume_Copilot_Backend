from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class JobBase(BaseModel):
    title: str = Field(..., max_length=255, description="Job title")
    company: str = Field(..., max_length=255, description="Company name")
    location: str = Field(..., max_length=255, description="Job location")
    employment_type: str = Field(..., description="Employment type (e.g. Full-Time, Internship)")
    source: str = Field(..., description="Job source (e.g. Linkedin)")
    url: str = Field(..., max_length=255, description="Job URL")
    description: str = Field(..., description="Job description")

class JobCreate(JobBase):
    application_status: str = Field(default="Not Started", description="Application status")
    parsed_requirements: dict | list | None = Field(default=None, description="Parsed requirements JSONB")

class JobResponse(JobBase):
    id: int
    application_status: str
    parsed_requirements: dict | list | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JobUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    employment_type: str | None = None
    source: str | None = None
    url: str | None = None
    description: str | None = None
    application_status: str | None = None
    parsed_requirements: dict | list | None = None
