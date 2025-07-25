from google import genai
from google.genai import types as genai_types
from typing import Optional
from src.llm.base import BaseLLMClient
from src.config import settings


class GeminiImageGeneration(BaseLLMClient):

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None) -> None:
        
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_IMAGE_MODEL_NAME

        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        self.client = genai.Client(api_key=self.api_key)

    def generate_image(
        self, 
        prompt: str, 
        max_tokens: int = 1000, 
        temperature: float = 1.0,
        **kwargs
    ) -> str:
        """Generate image using the Gemini API"""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=genai_types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],
                    safety_settings=settings.SAFETY_SETTINGS,
                    temperature=temperature,
                    top_p=1,
                    top_k=32,
                    max_output_tokens=max_tokens,
                )
            )
            
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")