from typing import Optional
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


class Settings(BaseSettings):
    # App Configuration
    APP_NAME: str = "Ad Generator MVP"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "A minimal viable product for ad generation using LLMs."
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["*"]
    
    # File Upload Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_TYPES: set[str] = {"image/jpeg", "image/png", "image/webp"}
    

    # LLM settings 
    LUNOS_API_KEY: str 
    LUNOS_BASE_URL: str = "https://api.lunos.tech/v1"
    DEFAULT_MODEL_NAME: str = "google/gemma-3-12b-it"

    # Gemini Image Generation settings
    GEMINI_API_KEY: str 
    GEMINI_IMAGE_MODEL_NAME: str = "gemini-2.0-flash-preview-image-generation"

    #  add safety settings
    SAFETY_SETTINGS: list[dict] = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour in seconds
    
    # Storage Configuration
    STORAGE_TYPE: str = "local"  # local, s3, cloudinary
    

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create upload directory if it doesn't exist
        Path(self.UPLOAD_DIR).mkdir(exist_ok=True)

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()