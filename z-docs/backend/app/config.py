from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Basic app settings
    APP_NAME: str = "Aegis Backend"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000

    # Database
    DB_URL: str = "sqlite:///./aegis.db"

    # Security
    FERNET_KEY_PATH: Path = Path(".fernet_key")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
