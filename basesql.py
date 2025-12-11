# common/sql_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# przykładowy connection string do PostgreSQL
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/video_rental"

class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    """Dependency / helper do uzyskania sesji (np. dla FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
