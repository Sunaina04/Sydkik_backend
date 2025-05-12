from fastapi import APIRouter, Depends, HTTPException
from app.crud.user_emails import add_user_email, get_user_emails, get_primary_email, update_user_email, delete_user_email
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db

router = APIRouter()

# Route to add an email
@router.post("/add_email")
async def add_email(user_id: str, email: str, is_primary: bool = False, db: AsyncSession = Depends(get_db)):
    try:
        new_email = await add_user_email(db, user_id, email, is_primary)
        return {"message": "Email added successfully", "email": new_email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to get all emails for a user
@router.get("/get_emails/{user_id}")
async def get_emails(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        emails = await get_user_emails(db, user_id)
        return {"emails": emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to get primary email for a user
@router.get("/get_primary_email/{user_id}")
async def get_primary(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        primary_email = await get_primary_email(db, user_id)
        if primary_email:
            return {"primary_email": primary_email}
        else:
            raise HTTPException(status_code=404, detail="Primary email not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to update an email
@router.put("/update_email/{email_id}")
async def update_email(email_id: str, new_email: str, is_primary: bool, db: AsyncSession = Depends(get_db)):
    try:
        updated_email = await update_user_email(db, email_id, new_email, is_primary)
        return {"message": "Email updated successfully", "email": updated_email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route to delete an email
@router.delete("/delete_email/{email_id}")
async def delete_email(email_id: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await delete_user_email(db, email_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
