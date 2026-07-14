from sqlalchemy.orm import relationship
from sqlalchemy import String,DateTime,func
from sqlalchemy.orm import Mapped,mapped_column
from app.database.base import Base
from app.models.resume import Resume

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False)
    email:Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
        )
    created_at:Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at:Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now()
    )

    resumes:Mapped[list["Resume"]] = relationship(
        back_populates="user",
        cascade="all,delete-orphan"
    )
    
        

    
