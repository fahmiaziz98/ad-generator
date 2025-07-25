from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum


 
class AdGenerationRequest(BaseModel):
    """Product input from user form"""
    # product information
    product_name: str = Field(..., min_length=1, max_length=200)
    brand_name: str = Field(None, max_length=100)
    category: List[str] = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    product_url: Optional[str] = Field(None, max_length=1000)

    # price
    price: Optional[float] = Field(None, gt=0)
    discounted_price: Optional[float] = Field(None, gt=0)
    
    # Image options
    image_url: Optional[str] = Field(None, description="URL of existing product image")
    # generate_image: bool = Field(False, description="Generate AI image for product")
    # include_image_in_ad: bool = Field(True, description="Include image reference in generated ad")
     
    # type and tone
    ad_type: Optional[str] = Field(None, max_length=50)
    ad_tone: Optional[str] = Field(None, max_length=50)


class ImageGenerationRequest(BaseModel):
    """Request model for standalone image generation"""
    product_name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10, max_length=1000)
    

class AdType(str, Enum):
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    PRODUCT_DESCRIPTION = "product_description"

class AdTone(str, Enum):
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional" 
    URGENT = "urgent"
    PLAYFUL = "playful"
    LUXURIOUS = "luxurious"
    MINIMALIST = "minimalist"
    BOLD = "bold"
    CONVERSATIONAL = "conversational"
