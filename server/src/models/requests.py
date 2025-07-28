from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class AdGenerationRequest(BaseModel):
    """Product input from user form"""
    # product information
    product_name: str = Field(..., min_length=1, max_length=200)
    brand_name: str = Field(None, max_length=100)
    category: List[str] = Field(..., min_length=1, max_length=100)
    description: str = Field(None)
    product_url: Optional[str] = Field(None, max_length=1000)

    # price
    price: Optional[float] = Field(None, gt=0)
    discounted_price: Optional[float] = Field(None, gt=0)
    
    # type and tone
    ad_type: Optional[str] = Field(None, max_length=50)
    ad_tone: Optional[str] = Field(None, max_length=50)


class ImageGenerationRequest(BaseModel):
    """Request model for standalone image generation"""
    product_name: str = Field(..., min_length=1, max_length=200)
    brand_name: str = Field(None, max_length=100)
    description: str = Field(None)
    

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
