from app.database.base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, DateTime, func, ForeignKey
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.resumeVersion import ResumeVersion

class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str | None] = mapped_column(String, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now()
    )

    user: Mapped["User"] = relationship(
        back_populates="resumes"
    )

    versions: Mapped[list["ResumeVersion"]] = relationship(
        cascade="all,delete-orphan",
        back_populates="resume"
    )

