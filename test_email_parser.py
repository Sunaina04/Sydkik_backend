import asyncio
import json
from app.services.email_processor import EmailProcessor

# Test emails
TEST_EMAILS = [
    {
        "subject": "Catch up?",
        "content": """Hey, hope you're doing well!

Do you have time to catch up sometime next week? I'm free most afternoons after 2pm.

Let me know what works best for you.

Cheers,  
Maya"""
    },
    {
        "subject": "Meeting on Thursday",
        "content": """Hi,

Can we have a 45-minute sync on Thursday at 10:30am? I'd like to walk you through the updated proposal.

Thanks,  
Raj"""
    },
    {
        "subject": "Need to Move Our Meeting",
        "content": """Hey,

I won't be able to make our meeting tomorrow at 4pm. Would Friday morning around 11 work instead?

Apologies for the change!  
— Laura"""
    },
    {
        "subject": "Let's talk",
        "content": """Hi there,

Let's set up a quick call sometime soon to go over the launch. I'm flexible next week, preferably early in the day.

Best,  
Chris"""
    }
]

async def test_email_parsing():
    processor = EmailProcessor()
    
    print("\n=== Testing Email Parser ===\n")
    
    for i, email in enumerate(TEST_EMAILS, 1):
        print(f"\n📧 Testing Email {i}")
        print(f"Subject: {email['subject']}")
        print("-" * 50)
        
        try:
            result = await processor.process_email(email['content'], email['subject'])
            print("Result:")
            print(json.dumps(result.model_dump(), indent=2))
        except Exception as e:
            print(f"Error processing email: {str(e)}")
        
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_email_parsing()) 