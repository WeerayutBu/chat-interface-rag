
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    VECTOR_DB_API_IP: str
    VECTOR_DB_API_KEY: str
    UI_CHAT_API_IP: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()