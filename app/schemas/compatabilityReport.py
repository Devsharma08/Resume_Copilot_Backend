from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Any


class CompatibilityReportBase(BaseModel):
    resume_version_id:int
    job_id:int

class CompatibilityReportCreate(CompatibilityReportBase):
    resume_version_id:int
    job_id:int
    match_score:int
    missing_skills:list[str]
    similarity_score:int
    feedback:dict[str,Any] | None

class CompatibilityReportResponse(CompatibilityReportBase):
    id:int
    resume_version_id:int
    job_id:int
    match_score:int
    missing_skills:list[str]
    similarity_score:int
    feedback:dict[str,Any] | None
    created_at:datetime
    model_config=ConfigDict(from_attributes=True)

class CompatibilityReportUpdate(CompatibilityReportBase):
    match_score:int | None
    missing_skills:list[str] | None
    similarity_score:int | None
    feedback:dict[str,Any] | None

class CompatibilityReportDelete(BaseModel):
    status:bool
    message:str
