import uuid
from io import BytesIO
from PIL import Image
from loguru import logger
from pathlib import Path
from typing import Optional, Tuple, Union

from google import genai
from google.genai import types as genai_types

from src.llm.base import BaseLLMClient
from src.config import settings


class GeminiImageGeneration(BaseLLMClient):

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None) -> None:
        
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_IMAGE_MODEL_NAME

        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        self.client = genai.Client(api_key=self.api_key)

    def _generate_image(
        self, 
        prompt: str,
        save_path: Optional[str] = None,
        **kwargs
    ) -> Optional[Union[Image.Image, Tuple[Image.Image, str]]]:
        """
        Generate image using Gemini 2.0 Flash Preview Image Generation
        
        Args:
            prompt: Text prompt for image generation
            save_path: Optional path to save the image
            
        Returns:
            PIL Image object or tuple of (Image, saved_path) if save_path provided
        """
        try:
            logger.info(f"Generating image with prompt: {prompt[:100]}...")
            
            # Generate content with Gemini
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=prompt,
                config=genai_types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],
                    safety_settings=self.safety_settings,
                    temperature=self.generation_config['temperature'],
                    top_p=self.generation_config['top_p'],
                    top_k=self.generation_config['top_k'],
                    max_output_tokens=self.generation_config['max_output_tokens'],
                )
            )
            
            # Process response parts
            generated_image = None
            response_text = None

            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    response_text = part.text
                    logger.info(f"Generated text: {response_text}")
                
                elif part.inline_data is not None:
                    # Convert binary data to PIL Image
                    image_data = part.inline_data.data
                    generated_image = Image.open(BytesIO(image_data))
                    logger.info(f"Generated image size: {generated_image.size}")
                    
                    # Save image if path provided
                    if save_path:
                        generated_image.save(save_path)
                        logger.info(f"Image saved to: {save_path}")
                        return generated_image, save_path
            
            if generated_image:
                logger.success("Image generation completed successfully")
                return generated_image
            else:
                logger.warning("No image data found in response")
                return None
                
        except Exception as e:
            logger.error(f"Error generating image with Gemini: {e}")
            return None

    def generate_image_save(
        self, 
        prompt: str, 
        product_name: Optional[str] = None,
        save_dir: Optional[str] = None,
        **kwargs
    ) -> Optional[Tuple[Image.Image, str, str]]:
        """
        Generate image and auto-save with generated filename
        
        Args:
            prompt: Text prompt for image generation
            product_name: Product name for filename generation
            save_dir: Directory to save (defaults to upload_dir)
            
        Returns:
            Tuple of (file_path, url_path, image_object) or None if failed
        """
        try:
            logger.info(f"Generating image for product: {product_name}...")
            if not save_dir:
                save_dir = settings.UPLOAD_DIR
            
            save_dir_path = Path(save_dir)
            save_dir_path.mkdir(parents=True, exist_ok=True)

            # Generate unique filename
            safe_product_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_product_name = safe_product_name.replace(' ', '_')[:30]  # Limit length
            
            filename = f"{uuid.uuid4().hex}_{safe_product_name}.png"
            file_path = save_dir_path / filename
            
            result = self._generate_image(prompt, save_path=str(file_path), **kwargs)
            
            if result:
                if isinstance(result, tuple):  # (Image, saved_path)
                    image_obj, saved_path = result
                    url_path = f"/static/{settings.UPLOAD_DIR}/{filename}"
                    return str(file_path), url_path, image_obj
                else:  # Just Image object
                    image_obj = result
                    image_obj.save(str(file_path))
                    url_path = f"/static/{settings.UPLOAD_DIR}/{filename}"
                    return str(file_path), url_path, image_obj
            
            return None
            
        except Exception as e:
            logger.error(f"Error in auto-save image generation: {e}")
            return None