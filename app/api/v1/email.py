from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.email_processor import EmailProcessor

router = APIRouter()
email_processor = EmailProcessor()

class EmailRequest(BaseModel):
    subject: str
    content: str
    sender: str

@router.post("/analyze")
async def analyze_email(email: EmailRequest):
    try:
        sender = email.sender 
        result = await email_processor.process_email(email.content, email.subject,sender)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 