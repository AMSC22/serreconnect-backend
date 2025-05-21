from pydantic_settings import BaseSettings
from typing import List
import json
import os

class Settings(BaseSettings):
    # Environment
    ENV: str = "development"
    DEBUG: bool = True

    # MongoDB Database
    MONGODB_URL: str = os.getenv("MONGO_URL")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME")
    MONGODB_AUTH_ENABLED: bool = False

    # Application Settings
    APP_NAME: str = os.getenv("APP_NAME")
    APP_VERSION: str = os.getenv("APP_VERSION")
    PORT: int = os.getenv("PORT")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    TIMEZONE: str = os.getenv("TIMEZONE") 
    SESSION_INACTIVITY_TIMEOUT_MINUTES: int = os.getenv("SESSION_INACTIVITY_TIMEOUT_MINUTES")  # Timeout d'inactivité

    # CORS Settings
    ALLOWED_ORIGINS: List[str]

    @classmethod
    def parse_allowed_origins(cls, value: str) -> List[str]:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return [origin.strip() for origin in value.split(",")]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "json_parsers": {
            List[str]: parse_allowed_origins
        }
    }

def get_settings() -> Settings:
    return Settings()

settings = get_settings()