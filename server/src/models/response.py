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

class ImageResult(BaseModel):
    """Internal model for image processing results"""
    image_path: Optional[str] = None  # Local file path (for uploaded/generated)
    image_url: Optional[str] = None  # URL for accessing the image
    source: str  # "uploaded", "url", "generated"
    generated: bool = False  # True if AI generated

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
