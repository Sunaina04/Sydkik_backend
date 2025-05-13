from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import text
from app.auth.config import oauth

router = APIRouter()

@router.get("/")
async def auth_root():
    return {"message": "Auth router is working"}

@router.get("/db-test")
async def test_db(db: AsyncSession = Depends(get_db)):
    try:
        query = text("SELECT 1")
        result = await db.execute(query)
        await db.commit()
        return {
            "status": "success",
            "message": "Database connection successful"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        } 

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback", name="auth_callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    print(token)
    id_token = token.get("id_token")
    if not id_token:
        raise HTTPException(status_code=400, detail="Missing id_token in token response")

    user_info = await oauth.google.parse_id_token(request, token)
    return {"user": user_info}