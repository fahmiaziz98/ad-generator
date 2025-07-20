from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from models.ad import ProductInput, AdType, AdTone
from .dependency import get_ad_generator


router = APIRouter(prefix="/ads", tags=["ads"])

@router.post("/generate/stream")
async def generate_ad_stream( 
    product: ProductInput,
    ad_generator=Depends(get_ad_generator)
):
    ad_type = AdType(product.ad_type) if product.ad_type else AdType.SOCIAL_MEDIA
    ad_tone = AdTone(product.ad_tone) if product.ad_tone else AdTone.FRIENDLY
    product_data = product.model_dump(exclude={"ad_type", "ad_tone"})
    product_str = "\n".join(f"{k}: {v}" for k, v in product_data.items() if v is not None)

    async def token_generator():
        try:
            async for token in ad_generator.generate(
                data_product=product_str,
                ad_type=ad_type,
                ad_tone=ad_tone
            ):
                yield token
        except Exception as e:
            yield f"\n[ERROR]: {str(e)}"

    return StreamingResponse(token_generator(), media_type="text/plain")