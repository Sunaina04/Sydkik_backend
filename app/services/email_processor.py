from typing import Dict, Optional
from pydantic import BaseModel
from app.config import settings
import google.generativeai as genai
import json
import asyncio
import functools
import time
from tenacity import retry, stop_after_attempt, wait_exponential

class MeetingDetails(BaseModel):
    is_scheduling: bool
    date: Optional[str] = None
    time: Optional[str] = None
    duration: Optional[str] = None
    subject: Optional[str] = None
    participants: Optional[list] = None
    intent: Optional[str] = None
    sender: Optional[str] = None 

class EmailProcessor:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("models/gemini-2.0-flash")
        self.last_request_time = 0
        self.min_request_interval = 10  # Increased to 10 seconds between requests
    @retry(
        stop=stop_after_attempt(2),  # Reduced retries for free API
        wait=wait_exponential(multiplier=1, min=5, max=15),  # Increased wait times
        reraise=True
    )
    async def process_email(self, email_content: str, subject: str,sender: str) -> MeetingDetails:
        prompt = self._create_prompt(email_content, subject)
        try:
            await self._wait_for_rate_limit()
            response = await self._async_generate_content(prompt)
            result = self._parse_ai_response(response)
            
            # Ensure participants is a list
            if result.get("participants") is None:
                result["participants"] = []
            elif isinstance(result["participants"], str):
                result["participants"] = [result["participants"]]
            result["sender"] = sender
            
            return MeetingDetails(**result)
        except Exception as e:
            if "429" in str(e):  # Rate limit error
                print(f"Rate limit hit, retrying after delay: {str(e)}")
                raise
            print(f"Error processing email: {str(e)}")
            return self._get_default_meeting_details(email_content, subject)

    async def _wait_for_rate_limit(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

    async def _async_generate_content(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            functools.partial(self.model.generate_content, prompt)
        )

    def _create_prompt(self, email_content: str, subject: str) -> str:
        return f"""
        Analyze this email and extract meeting scheduling information:

        Subject: {subject}
        Content: {email_content}

        Return a JSON object with the following structure:
        {{
            "is_scheduling": boolean,
            "date": "extracted date or null",
            "time": "extracted time or null",
            "duration": "extracted duration or null",
            "subject": "meeting subject or null",
            "participants": ["list of participants or empty list"],
            "intent": "schedule/reschedule/check_availability"
        }}

        Guidelines:
        - Set is_scheduling to true if the email is about scheduling, rescheduling, or checking availability
        - Extract specific dates and times when mentioned
        - Include duration if explicitly stated
        - For participants, include any mentioned groups (like 'team', 'everyone') and specific names
        - Identify the main intent of the email
        - Only include fields that are explicitly mentioned in the email
        """

    def _parse_ai_response(self, response) -> Dict:
        try:
            text = response.text
            text = text.replace("```json", "").replace("```", "").strip()
            result = json.loads(text)
            
            # Ensure participants is always a list
            if "participants" not in result:
                result["participants"] = []
            elif isinstance(result["participants"], str):
                result["participants"] = [result["participants"]]
            
            return result
        except Exception as e:
            print(f"Error parsing AI response: {str(e)}")
            return {"is_scheduling": False, "participants": []}

    def _get_default_meeting_details(self, email_content: str, subject: str) -> MeetingDetails:
        """Get default meeting details based on basic content analysis"""
        scheduling_keywords = [
            "schedule", "meeting", "appointment", "call", "sync",
            "reschedule", "availability", "when", "time", "date"
        ]
        
        content_lower = (email_content + " " + subject).lower()
        is_scheduling = any(keyword in content_lower for keyword in scheduling_keywords)
        
        # Extract basic participants
        participants = []
        if "team" in content_lower or "everyone" in content_lower:
            participants.append("team")
        
        return MeetingDetails(
            is_scheduling=is_scheduling,
            date=None,
            time=None,
            duration=None,
            subject=subject if is_scheduling else None,
            participants=participants,
            intent=None
        ) 