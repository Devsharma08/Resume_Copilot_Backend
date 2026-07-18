from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Any
class ResumeAnalyticsBase(BaseModel):
    resume_version_id:int

class ResumeAnalyticsCreate(ResumeAnalyticsBase):
    resume_version_id:int
    ats_score:int
    grammar_score:int
    keyword_score:int
    formatting_score:int
    overall_score:int
    feedback:dict[str,Any] | None

    model_config = ConfigDict(from_attributes=True)

class ResumeAnalyticsResponse(ResumeAnalyticsBase):
    id:int
    resume_version_id:int
    ats_score:int
    grammar_score:int
    keyword_score:int
    formatting_score:int
    overall_score:int
    feedback:dict[str,Any] | None
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)

class ResumeAnalyticsUpdate(ResumeAnalyticsBase):
    ats_score:int | None
    grammar_score:int | None
    keyword_score:int | None
    formatting_score:int | None
    overall_score:int | None
    feedback:dict[str,Any] | None

    model_config = ConfigDict(from_attributes=True)