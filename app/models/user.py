from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import TEXT
from app.models.base import Base
import datetime

class User(Base):
    __tablename__ = "users"

    sub = Column(String, primary_key=True, index=True)  # Google ID (unique)
    email = Column(String, unique=True, index=True)
    google_id = Column(String, unique=True, index=True) 
    name = Column(String)
    given_name = Column(String)
    picture = Column(TEXT)
    email_verified = Column(Boolean, default=False)
    access_token = Column(TEXT)
    refresh_token = Column(TEXT)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
