from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    # Environment
    ENV: str = "development"
    DEBUG: bool = True

    # MongoDB Database
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "serreconnect"
    MONGODB_AUTH_ENABLED: bool = False

    # Application Settings
    APP_NAME: str = "SerreConnect"
    APP_VERSION: str = "1.0.0"
    JWT_SECRET_KEY: str = "dev_secret_key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TIMEZONE: str = "Europe/Paris" 
    SESSION_INACTIVITY_TIMEOUT_MINUTES: int = 60  # Timeout d'inactivité

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