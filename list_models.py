import google.generativeai as genai
from app.config import settings

def list_available_models():
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model: {m.name}")
            print(f"Display name: {m.display_name}")
            print(f"Description: {m.description}")
            print(f"Generation methods: {m.supported_generation_methods}")
            print("-" * 50)

if __name__ == "__main__":
    list_available_models() 