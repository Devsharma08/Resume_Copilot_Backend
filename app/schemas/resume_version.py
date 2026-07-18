from typing import Any,Literal
from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field




class ResumeVersionBase(BaseModel):
    resume_id:int
    user_id:int
    status:str

class ResumeVersionCreate(ResumeVersionBase):
    version_number:int = Field(
        ...,
        description="The version number of the resume"
    )
    storage_key:str= Field(
        ...,
        max_length=255,
        description="Storage key for the resume version"
    )
    original_filename:str= Field(
        ...,
        max_length=255,
        description="Original filename of the resume version"
    )
    raw_text:str= Field(
        ...,
        description="The raw text of the resume version"
    )
    parsed_resume:dict[str,Any] | None= Field(
        None,
        description="The parsed resume of the resume version"
    )
    status:Literal["draft","active","archived"] = Field(
        default = "draft",
        description="The status of the resume version"
    )

class ResumeVersionUpdate(BaseModel):
    version_number:int | None= Field(
        None,
        description="The version number of the resume"
    )
    raw_text:str| None= Field(
        None,
        description="The raw text of the resume version"
    )
    parsed_resume:dict[str,Any]| None= Field(
        None,
        description="The parsed resume of the resume version"
    )
    status:Literal["draft","active","archived"] = Field(
        default="draft",
        description="The status of the resume version"
    )

    model_config = ConfigDict(from_attributes=True)

class ResumeVersionResponse(ResumeVersionBase):
    version_number:int
    id:int
    storage_key:str
    original_filename:str
    raw_text:str
    parsed_resume:dict[str,Any] | None
    status:str
    created_at:datetime
    updated_at:datetime
    model_config = ConfigDict(from_attributes=True)

class ResumeVersionDelete(BaseModel):
    status:bool
    message:str

    model_config = ConfigDict(from_attributes=True)

