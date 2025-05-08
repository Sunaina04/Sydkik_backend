from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    SECRET_KEY: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()
