from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select
from app.models.user import User
import datetime
import logging

logger = logging.getLogger(__name__)

# Create
async def create_user(db: AsyncSession, user_data: dict):
    db_user = User(
        sub=user_data['sub'], 
        email=user_data['email'],
        google_id=user_data['google_id'],
        name=user_data['name'],
        given_name=user_data['given_name'],
        picture=user_data['picture'],  # Storing the profile picture URL
        email_verified=user_data['email_verified'],
        access_token=user_data['access_token'],
        refresh_token=user_data['refresh_token'],
        created_at=user_data['created_at']  # We assume 'created_at' is passed as a datetime object
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

# Read (Fetch User by Google ID)
async def get_user_by_google_id(db: AsyncSession, google_id: str):
    try:
        result = await db.execute(select(User).filter(User.google_id == google_id))
        user = result.scalars().first()
        return user
    except Exception as e:
        logger.error(f"Error retrieving user by google_id {google_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching user")


# Update (For example, updating the user's email)
async def update_user_email(db: AsyncSession, google_id: str, new_email: str) -> User:
    user = await get_user_by_google_id(db, google_id)
    if user:
        user.email = new_email
        await db.commit()
        await db.refresh(user)  # Refresh the user instance after commit
        return user
    else:
        return None

# Delete (Remove a user by Google ID)
async def delete_user(db: AsyncSession, google_id: str) -> bool:
    user = await get_user_by_google_id(db, google_id)
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False
