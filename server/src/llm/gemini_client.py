from PIL import Image
from loguru import logger
from typing import Optional, Tuple, Union
from google import genai
from google.genai import types as genai_types

from src.llm.base import BaseLLMClient
from src.config import settings


class GeminiImageGeneration(BaseLLMClient):
    """
    GeminiImageGeneration is a client for interacting with the Gemini 2.0 Flash Preview Image Generation
    It supports generating images based on text prompts.
    It requires an API key and a model name to be initialized.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None) -> None:
        
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_IMAGE_MODEL_NAME

        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        self.client = genai.Client(api_key=self.api_key)

    def generate_image(
        self, 
        prompt: str,
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
                model=self.model_name,
                contents=prompt,
                config=genai_types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],
                    temperature=1.0,
                    top_p=1,
                    top_k=32,
                    max_output_tokens=1024,
                )
            )
            return response
        except Exception as e:
            logger.error(f"Error generating image with Gemini: {e}")
            return None
    
    def generate_text(self):
        pass

    def generate_text_streaming(self):
        pass

    def health_check(self):
        return super().health_check()
