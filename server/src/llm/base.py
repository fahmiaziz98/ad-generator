from abc import ABC, abstractmethod
from typing import AsyncIterator

class BaseLLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    async def generate_text(
        self, 
        prompt: str, 
        max_tokens: int = 1000, 
        temperature: float = 1,
        **kwargs
    ) -> str:
        """Generate text response"""
        pass
    
    @abstractmethod
    async def generate_text_streaming(
        self, 
        prompt: str, 
        max_tokens: int = 1000, 
        temperature: float = 1,
        stream: bool = True,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate text with streaming response"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the LLM service is healthy"""
        pass