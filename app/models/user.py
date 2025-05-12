from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime
import uuid


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

    # Define a relationship for the emails associated with a user
    emails = relationship("UserEmail", back_populates="user")


class UserEmail(Base):
    __tablename__ = "user_emails"  # Name of the table storing user emails

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_sub = Column(String, ForeignKey("users.sub"), nullable=False)  # ForeignKey to User's 'sub' column
    email = Column(String, nullable=False, unique=True)
    is_primary = Column(Boolean, default=False)  # Mark one email as primary

    # Define the reverse relationship back to the user
    user = relationship("User", back_populates="emails")
