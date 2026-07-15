from sqlalchemy import DateTime, String, func, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database.base import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.compatibilityReport import CompatibilityReport
    from app.models.coverLetter import CoverLetter
    from app.models.application import Application

class Job(Base):
    __tablename__ = "jobs"
    
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    company: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    employment_type: Mapped[str] = mapped_column(
        Enum("Full-Time", "Part-Time", "Contract", "Internship", "Other", name="employment_type_enum"),
        nullable=False
    )
    source: Mapped[str] = mapped_column(
        Enum("Linkedin", "Internshala", "Other", "Indeed", "Naukri", "TimesJob", "Whatsapp", name="source_enum"),
        nullable=False
    )
    url: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    application_status: Mapped[str] = mapped_column(
        Enum("Not Started", "In Progress", "Submitted", "Rejected", "Withdrawn", name="application_status_enum"),
        nullable=False,
        default="Not Started"
    )
    
    parsed_requirements: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=func.now(),
        server_default=func.now()
    )

    compatibility_reports: Mapped[list["CompatibilityReport"]] = relationship(
        back_populates="job",
        cascade="all,delete-orphan"
    )

    cover_letters: Mapped[list["CoverLetter"]] = relationship(
        back_populates="job",
        cascade="all,delete-orphan"
    )

    applications: Mapped[list["Application"]] = relationship(
        back_populates="job",
        cascade="all,delete-orphan"
    )

    
