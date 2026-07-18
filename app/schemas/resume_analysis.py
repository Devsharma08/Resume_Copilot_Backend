from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Any

class ResumeAnalysisBase(BaseModel):
    resume_version_id: int

class ResumeAnalysisCreate(ResumeAnalysisBase):
    ats_score: int
    grammar_score: int
    keyword_score: int
    formatting_score: int
    overall_score: int
    feedback: dict[str, Any] | None

class ResumeAnalysisResponse(ResumeAnalysisBase):
    id: int
    ats_score: int
    grammar_score: int
    keyword_score: int
    formatting_score: int
    overall_score: int
    feedback: dict[str, Any] | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ResumeAnalysisUpdate(BaseModel):
    ats_score: int | None = None
    grammar_score: int | None = None
    keyword_score: int | None = None
    formatting_score: int | None = None
    overall_score: int | None = None
    feedback: dict[str, Any] | None = None