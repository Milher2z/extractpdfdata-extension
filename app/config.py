from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "PDF Extractor API"
    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str = "sqlite:///./db/database.db"

    UPLOAD_DIR: Path = Path("./uploads")

    class Config:
        env_file = ".env"


settings = Settings()

settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
