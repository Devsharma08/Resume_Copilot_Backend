from enum import auto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    echo=True,
    url=settings.DATABASE_URL
)

sessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

db = sessionmaker()
