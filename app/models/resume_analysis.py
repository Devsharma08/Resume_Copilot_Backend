from sqlalchemy import DateTime, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database.base import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.resume_version import ResumeVersion



class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"
    
    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    resume_version_id: Mapped[int] = mapped_column(
        ForeignKey("resume_versions.id"),
        unique=True,
        nullable=False
    )
    ats_score: Mapped[int] = mapped_column(
        nullable=False
    )
    grammar_score: Mapped[int] = mapped_column(
        nullable=False
    )
    keyword_score: Mapped[int] = mapped_column(
        nullable=False
    )
    formatting_score: Mapped[int] = mapped_column(
        nullable=False
    )
    overall_score: Mapped[int] = mapped_column(
        nullable=False
    )
    feedback: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    resume_version: Mapped["ResumeVersion"] = relationship(
        back_populates="analysis"
    )