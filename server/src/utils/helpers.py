import uuid
import re
from typing import Optional
from urllib.parse import urlparse
from fastapi import HTTPException
from src.config import settings


class ImageValidator:
    """Utility class for validating image URLs, file extensions, and sizes."""
    @staticmethod
    def validate_image_url(url: str) -> bool:
        """Validate if the URL is a valid image URL."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
        except Exception:
            return False
        
    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        """Validate if the file extension is allowed."""
        if not filename:
            return False
        extension = '.' + filename.split('.')[-1].lower()
        return extension in settings.ALLOWED_FILE_EXTENSIONS
    
    @staticmethod
    def validate_image_type(content_type: Optional[str]) -> bool:
        """Validate if the content type is an allowed image type."""
        if not content_type:
            return False
        return content_type in settings.ALLOWED_IMAGE_TYPES
    
    @staticmethod
    def validate_image_size(file_size: int) -> bool:
        """Validate if the file size is within the allowed limit."""
        return file_size <= settings.MAX_FILE_SIZE
        
def generate_request_id() -> str:
    """Generate a unique request ID for tracking"""
    return str(uuid.uuid4())

