from loguru import logger
from typing import Optional
from src.core.image_generator import ImageGenerator
from src.models.requests import ImageGenerationRequest
from src.models.response import ImageResult

class ImageService:
    """
    Service to handle image generation requests.
    This service uses the ImageGenerator class to create images based on product details.
    """ 

    def __init__(self):
        self.image_generator = ImageGenerator()
    
    def generate_image(self, request: ImageGenerationRequest) -> Optional[ImageResult]:
        """
        Generate an image based on the provided request details.
        Args:
            request: ImageGenerationRequest containing product details. 
        Returns:
            ImageResult containing the path to the generated image or None if generation failed.
        """
        try:
            logger.info(f"Starting image generation for product: {request.product_name}, brand: {request.brand_name}")
            path_file = self.image_generator.generate_image_prompt(
                product_name=request.product_name,
                brand_name=request.brand_name,
                product_description=request.description
            )
            if path_file:
                logger.info(f"Image generated successfully: {path_file}")
                return ImageResult(
                    image_path=path_file,  # No local path for generated images
                    image_url=None,
                    source="generated",
                    generated=True
                )
            else:
                logger.error("Failed to generate image")
                return None
        except Exception as e:
            logger.critical(f"Critical error during image generation: {e}")
            return None

# Singleton service instance
_imagen_service_instance: Optional[ImageService] = None

def get_imagen_service() -> ImageService:
    """Get singleton ad service instance"""
    global _imagen_service_instance
    if _imagen_service_instance is None:
        _imagen_service_instance = ImageService()
    return _imagen_service_instance