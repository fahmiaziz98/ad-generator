import openai
from openai import AsyncOpenAI
from typing import Optional, AsyncIterator
from src.config import settings
from src.llm.base import BaseLLMClient


class OpenAIClient(BaseLLMClient):
    """
    OpenAIClient is a client for interacting with the OpenAI API.
    It supports both synchronous and asynchronous operations for generating text and streaming responses.
    It requires an API key and a model name to be initialized.
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None) -> None:
        """
        Initialize the OpenAIClient with an API key and model name.
        If no API key is provided, it will use the one from settings.
        If no model name is provided, it defaults to "google/gemma-3-12b-it".
        """
        self.api_key = api_key or settings.LUNOS_API_KEY
        self.model_name = model_name or settings.DEFAULT_MODEL_NAME

        if not self.api_key:
            raise ValueError("Lunos API key is required")
        
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=settings.LUNOS_BASE_URL
        )
    async def generate_text(
        self, 
        system: str,
        data_product: str, 
        max_tokens: int = 1000, 
        temperature: float = 1.0,
        **kwargs
    ) -> str:
        """Generate text using the OpenAI API"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": data_product}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            
            return response.choices[0].message.content.strip()
            
        except openai.APIError as e:
            raise Exception(f"Lunor API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Text generation failed: {str(e)}")
    

    async def generate_text_streaming(
            self, 
            system: str, 
            data_product: str,
            max_tokens: int = 1000, 
            temperature: float = 1.0,
            stream: bool = True,
            **kwargs
        ) -> AsyncIterator[str]:
        """Generate text with streaming response"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": data_product}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream,
                **kwargs
            )
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except openai.APIError as e:
            raise Exception(f"Lunor API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Text generation streaming failed: {str(e)}")
        
    async def health_check(self) -> bool:
        """Check if OpenAI API is accessible"""
        try:
            # Simple test request
            await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            return True
        except Exception:
            return False