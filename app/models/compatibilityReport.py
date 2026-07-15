from app.database.base import Base
from sqlalchemy import DateTime, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.resumeVersion import ResumeVersion


class CompatibilityReport(Base):
    __tablename__ = "compatibility_reports"
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    
    resume_version_id: Mapped[int] = mapped_column(
        ForeignKey("resume_versions.id"),
        nullable=False
    )
    
    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id"),
        nullable=False
    )
    
    compatibility_score: Mapped[int] = mapped_column(
        nullable=False
    )

    matched_skills: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )

    missing_skills: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )

    keyword_matches: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )

    recommendations: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    job: Mapped["Job"] = relationship(
        back_populates="compatibility_reports"
    )

    resume_version: Mapped["ResumeVersion"] = relationship(
        back_populates="compatibility_reports"
    )