from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from decimal import Decimal

 
class ProductInput(BaseModel):
    """Product input from user form"""
    product_name: str = Field(..., min_length=1, max_length=200)
    brand_name: str = Field(None, max_length=100)
    category: List[str] = Field(..., min_length=1, max_length=100)
    price: Optional[Decimal] = Field(None, gt=0)
    discounted_price: Optional[Decimal] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=1000)
    image_url: Optional[str] = Field(None, max_length=1000)
    product_url: Optional[str] = Field(None, max_length=1000)
    ad_type: Optional[str] = Field(None, max_length=50)
    ad_tone: Optional[str] = Field(None, max_length=50)


class AdType(str, Enum):
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    PRODUCT_DESCRIPTION = "product_description"

class AdTone(Enum):
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional" 
    URGENT = "urgent"
    PLAYFUL = "playful"
    LUXURIOUS = "luxurious"
    MINIMALIST = "minimalist"
    BOLD = "bold"
    CONVERSATIONAL = "conversational"
