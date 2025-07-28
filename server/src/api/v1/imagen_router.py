from loguru import logger
from pathlib import Path
from typing import Annotated
from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends
)

from fastapi.responses import FileResponse

from src.models.requests import ImageGenerationRequest
from src.models.response import ImageResult
from src.service.imagen_service import get_imagen_service, ImageService
from src.config import settings
from src.utils.helpers import generate_request_id


router = APIRouter(prefix=settings.API_V1_PREFIX, tags=["Image Generation"])

@router.post(
    "/generate-image",
    response_model=ImageResult,
    summary="Generate Image",
    description="Generate an image based on product details"
)
async def generate_image(
    request: ImageGenerationRequest,
    imagen_service: Annotated[ImageService, Depends(get_imagen_service)],
):
    """
    Generate an image based on the provided product details.
    
    Parameters:
    - request: ImageGenerationRequest containing product details.
    
    Returns:
    - ImageResult with generated image URL and metadata.
    """
    try:
        result = imagen_service.generate_image(request)
        if result is None:
            raise HTTPException(status_code=500, detail="Image generation failed")
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "image_generation_failed",
                "message": str(e),
                "request_id": generate_request_id()
            }
        )

from pathlib import Path

@router.get(
    "/images/{file_name}",
    summary="Get Image",
    description="Retrieve an image by its file name"
)
async def get_image(file_name: str):
    """
    Retrieve an image by its file name.
    
    Parameters:
    - file_name: Name of the image file to retrieve.
    
    Returns:
    - Image file if found, otherwise raises HTTP 404 error.
    """
    logger.info(f"Retrieving image: {file_name}")
    try:
        upload_dir = Path(settings.UPLOAD_DIR)
        file_path = upload_dir / file_name

        if not file_path.exists():
            logger.warning(f"Image not found: {file_name}")
            raise HTTPException(status_code=404, detail="Image not found")
        
        logger.info(f"Image retrieved successfully: {file_name}")
        return FileResponse(
            path=file_path,
            media_type="image/png",
            filename=file_name
        )
    except Exception as e:
        logger.critical(f"Critical error during image retrieval: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "image_retrieval_failed",
                "message": str(e),
                "request_id": generate_request_id()
            }
        )