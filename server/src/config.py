from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


class Settings(BaseSettings):
    # App settings
    app_name: str = "Ad Generator MVP"
    app_version: str = "1.0.0"
    debug: bool = True

    # LLM settings 
    LUNOS_API_KEY: str 
    lunos_base_url: str = "https://api.lunos.tech/v1"
    gemini_api_key: Optional[str] = "gemini_api_key"

    # Cache settings
    cache_ttl: int = 3600  # 1 hour

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()