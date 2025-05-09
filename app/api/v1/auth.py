from fastapi import APIRouter, Depends, Request, HTTPException
from app.crud.user import create_user, get_user_by_google_id
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import text
from app.auth.config import oauth
from jose import jwt


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
async def auth_callback(request: Request, db: AsyncSession = Depends(get_db)):
    # Get the token using OAuth2
    token = await oauth.google.authorize_access_token(request)
    id_token = token.get("id_token")
    
    if not id_token:
        raise HTTPException(status_code=400, detail="Missing id_token in token response")
    
    user_info = jwt.get_unverified_claims(id_token)

    # Check if user already exists
    existing_user = await get_user_by_google_id(db, user_info["sub"])

    if existing_user:
        return {"message": "User already exists", "user": existing_user}

    # Create new user if doesn't exist
    new_user = await create_user(db, {
        'sub': user_info['sub'],
        'email': user_info['email'],
        'name': user_info['name'],
        'given_name': user_info['given_name'],
        'picture': user_info['picture'],
        'email_verified': user_info['email_verified'],
        'access_token': token.get('access_token'),
        'refresh_token': token.get('refresh_token'),
        'created_at': user_info['iat']
    })

    return {"message": "User created successfully", "user": new_user}