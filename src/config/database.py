from sqlalchemy.orm import sessionmaker
from src.config.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URI = settings.DATABASE_URI

engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()