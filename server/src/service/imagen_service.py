from loguru import logger
from fastapi import UploadFile
from typing import Optional
from pathlib import Path

from src.config import settings
from src.core.image_generator import ImageGenerator
from src.core.processor.image_processor import ImageProcessor
from src.models.response import ImageResult

class ImageService:
    def __init__(self):
        self.image_generator = ImageGenerator()
        self.image_processor = ImageProcessor()

    def process_image_request(
        self,
        product_name: str,
        brand_name: Optional[str],
        description: str,
        image_url: Optional[str] = None,
        uploaded_file: Optional[UploadFile] = None,
        generate_image: bool = False
    ) -> Optional[ImageResult]:
        """
        Process image request with multiple input options:
        1. Use provided image_url
        2. Process uploaded file
        3. Generate AI image
        4. No image (return None)
        
        Priority: uploaded_file > image_url > generate_image
        """
        try:
            if uploaded_file:
                logger.info("Processing uploaded image file")
                results = self.image_generator.validate_and_process_uploaded_image(uploaded_file, product_name)
                
                if results:
                    image_path, image_url = results
                    
                    return ImageResult(
                        image_path=image_path, 
                        image_url=image_url, 
                        source="uploaded", 
                        generated=False
                    )
                else:
                    logger.error("Failed to process uploaded image file")
                    return None
            if image_url:
                    logger.info(f"Using provided image URL: {image_url}")
                    # Validate URL format
                    if self.image_processor.validate_image_url(image_url):
                        return ImageResult(
                            image_path=None,
                            image_url=image_url,
                            source="url",
                            generated=False
                        )
                    else:
                        logger.warning(f"Invalid image URL: {image_url}")
                        return None
            if generate_image:
                    logger.info(f"Generating AI image for product: {product_name}")
                    result = self.image_generator.generate_image_prompt(
                        product_name=product_name,
                        brand_name=brand_name,
                        product_description=description
                    )
                    if result:
                        image_path, image_url_result = result
                        return ImageResult(
                            image_path=image_path,
                            image_url=image_url_result,
                            source="generated",
                            generated=True
                        )
                    else:
                        logger.error("Failed to generate AI image")
                        return None
                    
            logger.info("No image provided or requested")
            return None  # No image to process, return None
        except Exception as e:
            logger.error(f"Error processing image request: {e}")
            return None
    
    def cleanup_temp_files(self, image_paths: list[str]):
        """Clean up temporary image files if needed"""
        try:
            for path in image_paths:
                if path and path.startswith(str(self.image_generator.upload_dir)):
                    # Only cleanup generated files, not uploaded ones
                    # Implement cleanup logic 
                    if Path(path).exists():
                        Path(path).unlink()
                        logger.info(f"Deleted temporary file: {path}")
                    else:
                        logger.warning(f"Temporary file not found: {path}")
        except Exception as e:
            logger.warning(f"Error cleaning up temp files: {e}")