from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from typing import TYPE_CHECKING

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.resume import Resume
    from app.models.resumeAnalysis import ResumeAnalysis
    from app.models.compatibilityReport import CompatibilityReport
    from app.models.coverLetter import CoverLetter

class ResumeVersion(Base):
    __tablename__ = "resume_versions"   
    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=False
    )
    
    version_number: Mapped[int] = mapped_column(
        nullable=False
    )

    storage_key: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    raw_text: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    parsed_resume: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False
    )
    
    status: Mapped[str] = mapped_column(
        String(50),
        default="Draft",
        nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    resume: Mapped["Resume"] = relationship(
        back_populates="versions"
    )

    analysis: Mapped["ResumeAnalysis | None"] = relationship(
        back_populates="resume_version",
        cascade="all,delete-orphan"
    )

    compatibility_reports: Mapped[list["CompatibilityReport"]] = relationship(
        back_populates="resume_version",
        cascade="all,delete-orphan"
    )

    cover_letters: Mapped[list["CoverLetter"]] = relationship(
        back_populates="resume_version",
        cascade="all,delete-orphan"
    )


