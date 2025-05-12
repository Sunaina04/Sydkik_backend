from fastapi import APIRouter, Depends, Request, HTTPException
from app.crud.user import create_user, get_user_by_google_id
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import text
from app.auth.config import oauth
from jose import jwt, JWTError
from fastapi import Header
import datetime
import logging
import secrets

# Initialize logger
logger = logging.getLogger(__name__)

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
        logger.error(f"Database connection failed: {str(e)}")
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }

@router.get("/login")
async def login(request: Request):
    nonce = secrets.token_urlsafe()
    request.session['nonce'] = nonce  # Store the nonce in session

    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri, nonce=nonce)

@router.get("/callback", name="auth_callback")
async def auth_callback(request: Request, db: AsyncSession = Depends(get_db)):
    # Get the token using OAuth2
    token = await oauth.google.authorize_access_token(request)
    id_token = token.get("id_token")

    if not id_token:
        logger.warning("Missing id_token in the response from Google OAuth")
        raise HTTPException(status_code=400, detail="Missing id_token in token response")

    nonce = request.session.get("nonce")
    if not nonce:
        raise HTTPException(status_code=400, detail="Missing nonce in session")

    try:
        # ✅ Pass nonce to validate the id_token
        user_info = await oauth.google.parse_id_token(token, nonce=nonce)
    except JWTError as e:
        logger.error(f"Error decoding or validating id_token: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid token: {str(e)}")
    
    # Check if the 'sub' (user ID) is present in the decoded token
    if "sub" not in user_info:
        logger.warning("Missing 'sub' in the decoded id_token")
        raise HTTPException(status_code=400, detail="Invalid token: 'sub' field missing")

    # Check if user already exists
    existing_user = await get_user_by_google_id(db, user_info["sub"])

    if existing_user:
        return {"message": "User already exists", "user": existing_user}

    # Create new user if doesn't exist
    created_at = datetime.datetime.utcfromtimestamp(user_info['iat'])  # Convert 'iat' to datetime

    try:
        user_info = {
            'sub': token['userinfo']['sub'],  
            'email': token['userinfo']['email'],
            'google_id': token['userinfo']['sub'],
            'name': token['userinfo']['name'],
            'given_name': token['userinfo']['given_name'],
            'picture': token['userinfo']['picture'],
            'email_verified': token['userinfo']['email_verified'],
            'access_token': token['access_token'],
            'refresh_token': token.get('refresh_token', None),  
            'created_at': created_at,
        }

        new_user = await create_user(db, user_info)
        return {"message": "User created successfully", "user": new_user}

    except Exception as e:
        logger.error(f"Error creating new user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while creating user")

def get_google_data_from_request(request: Request):
    # Extract necessary data from the request
    # Example: Extract a 'google_id' from cookies or session (if needed)
    google_id = request.cookies.get('google_id')  # Example
    return {
        'google_id': google_id
    }

@router.get("/me")
async def get_me(authorization: str = Header(...), db: AsyncSession = Depends(get_db)):
    try:
        token = authorization.replace("Bearer ", "")
        user_info = await oauth.google.parse_id_token({'id_token': token})
        user = await get_user_by_google_id(db, user_info["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user": user}
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@router.get("/get-email/{google_id}")
async def get_email(google_id: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_google_id(db, google_id)
    if user:
        return {"email": user.email}
    raise HTTPException(status_code=404, detail="User not found")
