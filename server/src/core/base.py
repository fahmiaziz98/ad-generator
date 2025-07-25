from abc import ABC, abstractmethod
from typing import AsyncIterator, Dict, Any
from src.models.requests import AdGenerationRequest


class BaseAdGenerator(ABC):
    """Abstract base class for ad generators"""
    
    @abstractmethod
    async def generate(self, request: AdGenerationRequest, **kwargs):
        """Generate advertisement"""
        pass
    
    @abstractmethod
    async def generate_streaming(self, request: AdGenerationRequest, **kwargs) -> AsyncIterator[Dict[str, Any]]:
        """Generate advertisement with streaming response"""
        pass