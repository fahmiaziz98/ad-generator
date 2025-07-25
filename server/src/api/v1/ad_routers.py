import json
from typing import Annotated
from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends
)
from fastapi.responses import StreamingResponse

from src.models import AdGenerationRequest, AdGenerationResponse
from src.service.ad_service import get_ad_service, AdService
from src.api.dependency import get_rate_limiter
from src.utils.helpers import generate_request_id
from src.config import settings


router = APIRouter(prefix=settings.API_V1_PREFIX, tags=["Advertisement Generation"])

@router.post(
    "/generate",
    response_model=AdGenerationResponse,
    summary="Generate Advertisement",
    description="Generate advertisement with optional image processing"
)
async def generate_ad(
    request: AdGenerationRequest,
    ad_service: Annotated[AdService, Depends(get_ad_service)],
    rate_limiter=Depends(get_rate_limiter),
):
    """
    Generate advertisement content based on the provided request.
    
    Parameters:
    - request: AdGenerationRequest containing product details and ad settings.
    
    Returns:
    - AdGenerationResponse with generated ad content and metadata.
    """
    try:
        response = await ad_service.generate_ad(request)
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "generation_failed",
                "message": str(e),
                "request_id": generate_request_id()
            }
        )

@router.post(
    "/generate-stream",
    summary="Generate Advertisement (Streaming)",
    description="Generate advertisement with streaming response"
)
async def generate_ad_streaming(
    request: AdGenerationRequest,
    ad_service: Annotated[AdService, Depends(get_ad_service)],
    rate_limiter=Depends(get_rate_limiter)
):
    """
    Generate advertisement content with streaming response.
    
    Parameters:
    - request: AdGenerationRequest containing product details and ad settings.
    
    Returns:
    - StreamingResponse with chunks of generated ad content.
    """
    async def stream_response():
        try:
            async for chunk in ad_service.generate_ad_streaming(request):
                yield json.dumps(chunk, default=str) + "\n"
        except Exception as e:
            error_response = {
                "status": "error",
                "error_code": "generation_failed",
                "message": str(e),
                "request_id": generate_request_id()
            }
            yield json.dumps(error_response) + "\n"

    return StreamingResponse(
        stream_response(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )