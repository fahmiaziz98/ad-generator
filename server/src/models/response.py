from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal, List
from decimal import Decimal

class ProductInfo(BaseModel):
    """Product information"""
    product_name: str
    brand: Optional[str]
    category: List[str]
    description: str
    price: Optional[Decimal]
    discounted_price: Optional[Decimal]
    store_link: str

class AdSettings(BaseModel):
    """Settings for ad generation"""
    ad_type: str = Field(..., description="Type of advertisement")
    ad_tone: str = Field(..., description="Tone of the advertisement")

class ImageInfo(BaseModel):
    """Image information in response"""
    has_image: bool = Field(description="Whether image is included")
    image_url: Optional[str] = Field(None, description="URL of the image")
    image_source: Optional[Literal["uploaded", "url", "ai_generated"]] = Field(
        None, description="Source of the image"
    )
    included_in_ad: bool = Field(False, description="Whether image is referenced in ad text")
    generation_time: Optional[float] = Field(None, description="Time taken to generate/process image")

class AdGenerationResponse(BaseModel):
    """Complete response for ad generation"""
    
    # Main content
    ad_content: str = Field(description="Generated advertisement content")
    
    # Metadata
    product_info: ProductInfo
    ad_settings: AdSettings
    # image_info: ImageInfo
    
    # Generation metadata
    generation_time: float = Field(description="Total generation time in seconds")
    model_used: str = Field(description="AI model used for generation")
    request_id: str = Field(description="Unique request identifier")
    timestamp: datetime = Field(default_factory=datetime.now)
