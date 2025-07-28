from PIL import Image
from io import BytesIO
from pathlib import Path
from typing import Optional
from loguru import logger

from src.llm.gemini_client import GeminiImageGeneration
from src.prompts.imagen_prompt import IMAGEN_PROMPT_TEMPLATE
from src.config import settings


class ImageGenerator:
    """
    Class to handle image generation using Gemini Image Generation API.
    This class provides methods to generate image prompts based on product details
    and save the generated images to a specified directory.
    """
    def __init__(self) -> None:
        self.imagen = GeminiImageGeneration()
        self.prompt_template = IMAGEN_PROMPT_TEMPLATE
        self.save_dir = Path(settings.UPLOAD_DIR)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def generate_image_prompt(
        self,
        product_name: str,
        brand_name: str,
        product_description: str
    ) -> Optional[str]:
        """
        Generate image prompt for the given product details.
        
        Args:
            product_name: Name of the product
            brand_name: Brand name of the product
            product_description: Description of the product
            
        Returns:
            Generated image prompt string
        """
        try:
            file_name = f"{product_name.replace(' ', '_')}_{brand_name.replace(' ', '_')}.png"
            file_path = self.save_dir / file_name
            prompt = self.prompt_template.format(
                product_name=product_name,
                brand_name=brand_name,
                product_description=product_description
            )

            response = self.imagen.generate_image(prompt=prompt)

            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    logger.info(f"Generated text: {part.text}")
                elif part.inline_data is not None:
                    image_data = part.inline_data.data
                    image = Image.open(BytesIO(image_data))
                    image.save(file_path)
                    logger.info(f"Image saved to: {file_path}")
                    return str(file_path)         
        except Exception as e:
            logger.error(f"Error generating image prompt: {e}")
            raise RuntimeError(f"Failed to generate image prompt: {e}")
            