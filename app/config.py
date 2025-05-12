from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    # Application settings
    SECRET_KEY: str
    
    # OAuth settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    
    # OpenAI settings
    OPENAI_API_KEY: str

    # AI Model settings
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
