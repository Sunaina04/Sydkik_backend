from fastapi import FastAPI
from app.api.v1 import auth, email
from starlette.middleware.sessions import SessionMiddleware
import secrets
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=secret_key)

@app.get("/")
def health_check():
    return {"status": "running"}

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(email.router, prefix="/api/v1/email", tags=["email"])

