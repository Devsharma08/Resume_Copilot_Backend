from app.database.base import Base
from sqlalchemy import DateTime, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.resumeVersion import ResumeVersion
    from app.models.job import Job

class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id: Mapped[int] = mapped_column(primary_key=True)
    resume_version_id: Mapped[int] = mapped_column(ForeignKey("resume_versions.id"), nullable=False)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    tone: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    resume_version: Mapped["ResumeVersion"] = relationship(back_populates="cover_letters")
    job: Mapped["Job"] = relationship(back_populates="cover_letters")
