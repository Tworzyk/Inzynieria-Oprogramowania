from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# Parametry pobierane z kontenera
DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/video_rental")

class Base(DeclarativeBase):
    pass

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()