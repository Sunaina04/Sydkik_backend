from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime
import uuid

class User(Base):
    __tablename__ = "users"

    sub = Column(String, primary_key=True, index=True)  
    email = Column(String, unique=True, index=True)
    google_id = Column(String, unique=True, index=True)
    name = Column(String)
    given_name = Column(String)
    picture = Column(TEXT)
    email_verified = Column(Boolean, default=False)
    access_token = Column(TEXT)
    refresh_token = Column(TEXT)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    emails = relationship("UserEmail", back_populates="user")


class UserEmail(Base):
    __tablename__ = "user_emails"  

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_sub = Column(String, ForeignKey("users.sub"), nullable=False)  
    email = Column(String, nullable=False, unique=True)
    is_primary = Column(Boolean, default=False)  
    user = relationship("User", back_populates="emails")
