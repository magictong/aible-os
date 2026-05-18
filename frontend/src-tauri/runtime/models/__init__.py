from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import DATABASE_URL
import re

# Convert async URL to sync URL for SQLite
_sync_url = re.sub(r'^sqlite\+aiosqlite:', 'sqlite:', DATABASE_URL)
engine = create_engine(_sync_url, echo=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

def init_db():
    from models.user import User
    from models.app import InstalledApp
    Base.metadata.create_all(engine)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()