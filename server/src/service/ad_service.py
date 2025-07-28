from typing import AsyncIterator, Dict, Any, Optional
from src.models import (
    AdGenerationRequest,
    AdGenerationResponse
)
from src.core.ad_generator import AIAdGenerator


class AdService:
    """
    Service to handle ad generation requests.
    This service uses the AIAdGenerator class to create ads based on product details.
    """
    def __init__(self) -> None:
        self.ad_generator = AIAdGenerator()

    async def generate_ad(self, request: AdGenerationRequest, **kwargs) -> AdGenerationResponse:
        """
        Generate an ad based on the provided request details.
        Args:
            request: AdGenerationRequest containing product details.
        Returns:
            AdGenerationResponse containing the generated ad content.
        """
        return await self.ad_generator.generate(request, **kwargs)

    async def generate_ad_streaming(
        self, 
        request: AdGenerationRequest, 
        **kwargs
    ) -> AsyncIterator[Dict[str, Any]]:
        """        
        Generate an ad in a streaming manner based on the provided request details.
        Args:
            request: AdGenerationRequest containing product details.
        Returns:
            AsyncIterator yielding chunks of AdGenerationResponse.
        """
        try:
            async for chunk in self.ad_generator.generate_streaming(request, **kwargs):
                yield chunk
        except Exception as e:
            yield {
                "status": "error",
                "message": str(e),
                "error_code": "service_error"
            }

# Singleton service instance
_ad_service_instance: Optional[AdService] = None

def get_ad_service() -> AdService:
    """Get singleton ad service instance"""
    global _ad_service_instance
    if _ad_service_instance is None:
        _ad_service_instance = AdService()
    return _ad_service_instance