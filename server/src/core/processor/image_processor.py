import re
from urllib.parse import urlparse
from typing import Optional
from loguru import logger
from pathlib import Path
from typing import Dict, Any
from fastapi import UploadFile

from src.config import settings


class ImageProcessor:
    def __init__(self):
        self.url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    def validate_image_url(self, url: str) -> bool:
        """
        Validate if URL is a proper image URL
        """
        try:
            if not url:
                return False
            
            if not self.url_pattern.match(url):
                return False
            
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            path = parsed.path.lower()
            
            if any(path.endswith(ext) for ext in settings.ALLOWED_FILE_EXTENSIONS):
                return True
            
            logger.info(f"URL validation passed: {url}")
            return True
        
        except Exception as e:
            logger.error(f"Error validating URL {url}: {e}")
            return False
    
    def validate_image_file(file: UploadFile) -> Dict[str, Any]:
        """
        Validate uploaded image file
        
        Returns:
            Dict with validation result and error message if any
        """
        try:
            if not file:
                return {"valid": False, "error": "No file provided"}
            
            file_extension = Path(file.filename).suffix.lower()
            if file_extension not in settings.ALLOWED_FILE_EXTENSIONS:
                return {
                    "valid": False,
                    "error": f"File extension '{file_extension}' not allowed. Allowed: {', '.join(settings.ALLOWED_FILE_EXTENSIONS)}"
                }
            
            # Check content type
            if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
                return {
                    "valid": False,
                    "error": f"Content type '{file.content_type}' not allowed. Allowed: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
                }
            
            # Check file size (read first chunk to check)
            file.file.seek(0, 2)  # Seek to end
            file_size = file.file.tell()
            file.file.seek(0)  # Reset to beginning
            
            if file_size > settings.MAX_FILE_SIZE:
                return {
                    "valid": False,
                    "error": f"File size ({file_size} bytes) exceeds maximum allowed size ({settings.MAX_FILE_SIZE} bytes)"
                }
            
            logger.info(f"File validation passed: {file.filename} ({file_size} bytes)")
            return {"valid": True, "file_size": file_size}
            
        except Exception as e:
            logger.error(f"Error validating file: {e}")
            return {"valid": False, "error": f"Validation error: {str(e)}"}


    def get_image_info(self, image_path: str) -> Optional[dict]:
        """
        Get basic image information (size, format, etc.)
        This can be expanded for image processing needs
        """
        try:
            from PIL import Image
            
            with Image.open(image_path) as img:
                return {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "mode": img.mode,
                    "size_bytes": len(open(image_path, 'rb').read())
                }
        except Exception as e:
            logger.error(f"Error getting image info for {image_path}: {e}")
            return None