from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, DateTime, func
from app.database.base import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.resume import Resume
    from app.models.application import Application

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=func.now(),
        server_default=func.now()
    )

    provider_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
        unique=True
    )

    resumes: Mapped[list["Resume"]] = relationship(
        cascade="all,delete-orphan",
        back_populates="user"
    )

    applications: Mapped[list["Application"]] = relationship(
        cascade="all,delete-orphan",
        back_populates="user"
    )
