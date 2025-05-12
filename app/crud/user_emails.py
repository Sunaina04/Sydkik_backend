from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import UserEmail
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

# Add email to a user
async def add_user_email(db: AsyncSession, user_id: str, email: str, is_primary: bool = False):
    try:
        new_email = UserEmail(user_id=user_id, email=email, is_primary=is_primary)
        db.add(new_email)
        await db.commit()
        await db.refresh(new_email)
        return new_email
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error adding email: {str(e)}")

# Fetch all emails for a user
async def get_user_emails(db: AsyncSession, user_id: str):
    try:
        result = await db.execute(select(UserEmail).filter(UserEmail.user_sub == user_id))
        emails = result.scalars().all()
        return emails
    except SQLAlchemyError as e:
        raise Exception(f"Error fetching emails: {str(e)}")

# Fetch primary email for a user
async def get_primary_email(db: AsyncSession, user_id: str):
    try:
        result = await db.execute(select(UserEmail).filter(UserEmail.user_id == user_id, UserEmail.is_primary == True))
        primary_email = result.scalars().first()
        return primary_email
    except SQLAlchemyError as e:
        raise Exception(f"Error fetching primary email: {str(e)}")

# Update a user's email (for example, make one primary)
async def update_user_email(db: AsyncSession, email_id: str, new_email: str, is_primary: bool):
    try:
        email = await db.get(UserEmail, email_id)
        if email:
            email.email = new_email
            email.is_primary = is_primary
            await db.commit()
            await db.refresh(email)
            return email
        else:
            raise Exception("Email not found")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error updating email: {str(e)}")

# Delete an email from the user's record
async def delete_user_email(db: AsyncSession, email_id: str):
    try:
        email = await db.get(UserEmail, email_id)
        if email:
            await db.delete(email)
            await db.commit()
            return {"message": "Email deleted successfully"}
        else:
            raise Exception("Email not found")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error deleting email: {str(e)}")
