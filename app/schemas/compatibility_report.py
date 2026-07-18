from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class CompatibilityReportBase(BaseModel):
    resume_version_id: int
    job_id: int

class CompatibilityReportCreate(CompatibilityReportBase):
    compatibility_score: int
    matched_skills: dict | list | None = None
    missing_skills: dict | list | None = None
    keyword_matches: dict | list | None = None
    recommendations: dict | list | None = None

class CompatibilityReportResponse(CompatibilityReportBase):
    id: int
    compatibility_score: int
    matched_skills: dict | list | None = None
    missing_skills: dict | list | None = None
    keyword_matches: dict | list | None = None
    recommendations: dict | list | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CompatibilityReportUpdate(BaseModel):
    compatibility_score: int | None = None
    matched_skills: dict | list | None = None
    missing_skills: dict | list | None = None
    keyword_matches: dict | list | None = None
    recommendations: dict | list | None = None
