from app.database.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import String,DateTime,func,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column



class Resume(Base):
    __tablename__ = "resumes"

    id:Mapped[int] = mapped_column(primary_key=True)

    title:Mapped[str] = mapped_column(String(255), nullable=False)

    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
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

    user:Mapped["User"] = relationship("User", back_populates="resumes")
    
