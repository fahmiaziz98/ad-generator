from typing import AsyncIterator, Dict, Any, Optional
from src.config import settings
from src.models import (
    AdGenerationRequest,
    AdGenerationResponse
)
from src.core.ad_generator import AIAdGenerator
from src.utils.helpers import generate_request_id


class AdService:
    """Service class for handling ad generation requests."""
    def __init__(self) -> None:
        self.ad_generator = AIAdGenerator()

    async def generate_ad(self, request: AdGenerationRequest, **kwargs) -> AdGenerationResponse:
        """Generate ad content based on the provided request."""
        return await self.ad_generator.generate(request, **kwargs)

    async def generate_ad_streaming(
        self, 
        request: AdGenerationRequest, 
        **kwargs
    ) -> AsyncIterator[Dict[str, Any]]:
        """Generate ad content with streaming response."""
        try:
            async for chunk in self.ad_generator.generate_streaming(request, **kwargs):
                yield chunk
        except Exception as e:
            yield {
                "status": "error",
                "message": str(e),
                "error_code": "service_error"
            }
    
    async def health_check(self) -> Dict[str, Any]:
        try:
            is_healthy = await self.ad_generator.llm.health_check()
            return {
                "status": "healthy" if is_healthy else "unhealthy",
                "model_name": self.ad_generator.llm.model_name,
                "version": settings.VERSION
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }

# Singleton service instance
_ad_service_instance: Optional[AdService] = None

def get_ad_service() -> AdService:
    """Get singleton ad service instance"""
    global _ad_service_instance
    if _ad_service_instance is None:
        _ad_service_instance = AdService()
    return _ad_service_instance