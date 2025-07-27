import os
import uuid
from pathlib import Path
from typing import Optional, Tuple
from loguru import logger

from src.llm.gemini_client import GeminiImageGeneration
from src.prompts.imagen_prompt import IMAGEN_PROMPT_TEMPLATE
from src.config import settings


class ImageGenerator:
    def __init__(self) -> None:
        self.imagen = GeminiImageGeneration()
        self.prompt_template = IMAGEN_PROMPT_TEMPLATE
        self.save_dir = Path(settings.UPLOAD_DIR)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def generate_image_prompt(
        self,
        product_name: str,
        brand_name: str,
        product_description: str,
        save_to_disk: bool = True
    ) -> Optional[Tuple[str, str]]:
        """
        Generate AI image for product
        
        Returns:
            Tuple[str, str]: (image_path, image_url) if successful, None if failed
        """
        try:
            prompt = self.prompt_template.format(
                product_name=product_name,
                brand_name=brand_name or "Generic Brand",
                product_description=product_description
            )
            
            logger.info(f"Generating image for product: {product_name}")
            
            if save_to_disk:
                result = self.imagen.generate_image_save(
                    prompt=prompt,
                    product_name=product_name,
                    save_dir=str(self.save_dir)
                )
                
                if result:
                    file_path, url_path, image_obj = result
                    logger.info(f"Image generated and saved: {file_path}")
                    logger.info(f"Image size: {image_obj.size}")
                    return file_path, url_path
                else:
                    logger.error("Failed to generate image with Gemini")
                    return None
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None

    def validate_and_process_uploaded_image(
        self, 
        uploaded_file,
        product_name: str
    ) -> Optional[Tuple[str, str]]:
        """
        Process uploaded image file
        
        Returns:
            Tuple[str, str]: (image_path, image_url) if successful, None if failed
        """
        try:
            # Generate unique filename
            file_extension = Path(uploaded_file.filename).suffix.lower()
            if file_extension not in settings.ALLOWED_FILE_EXTENSIONS:
                raise ValueError(f"File extension {file_extension} not allowed")
            
            image_filename = f"{uuid.uuid4().hex}_{product_name.replace(' ', '_')}{file_extension}"
            image_path = self.upload_dir / image_filename
            
            # Save uploaded file
            with open(image_path, "wb") as buffer:
                content = uploaded_file.file.read()
                if len(content) > settings.MAX_FILE_SIZE:
                    raise ValueError("File size exceeds maximum allowed size")
                buffer.write(content)
            
            # Create URL path
            image_url = f"/static/uploads/{image_filename}"
            
            logger.info(f"Uploaded image saved to: {image_path}")
            return str(image_path), image_url
            
        except Exception as e:
            logger.error(f"Error processing uploaded image: {e}")
            return None         