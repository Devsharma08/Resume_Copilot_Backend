from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime
from enum import Enum

class JobStatus(str,Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    EXPIRED = "expired"


class JobBase(BaseModel):
    title:str = Field(...,max_length=255,description="Job title")
    company_name:str = Field(...,max_length=255,description="Company name")
    location:str | None = Field(None,max_length=255,description="Job location")
    description:str = Field(...,description="Job description")
    requirements:str = Field(...,description="Job requirements")
    responsibilities:str = Field(...,description="Job responsibilities")
    status:JobStatus = Field(default=JobStatus.ACTIVE,description="Job status")


class JobCreate(JobBase):
    url:str | None = Field(None,max_length=255,description="Job URL")
    source:str | None = Field(None,max_length=255,description="Job source")

class JobDelete(BaseModel):
    status:bool
    message:str

    model_config = ConfigDict(from_attributes=True)

class JobUpdate(BaseModel):
    title:str | None = Field(None,max_length=255,description="Job title")
    company_name:str | None = Field(None,max_length=255,description="Company name")
    location:str | None = Field(None,max_length=255,description="Job location")
    description:str | None = Field(None,description="Job description")
    requirements:str | None = Field(None,description="Job requirements")
    responsibilities:str | None = Field(None,description="Job responsibilities")
    status:JobStatus | None = Field(None,description="Job status")
    url:str | None = Field(None,max_length=255,description="Job URL")


class JobResponse(BaseModel):
    id:int
    title:str
    company_name:str
    location:str | None
    description:str
    requirements:str
    responsibilities:str
    status:JobStatus
    created_at:datetime
    updated_at:datetime
    url:str | None

    model_config = ConfigDict(from_attributes=True)
