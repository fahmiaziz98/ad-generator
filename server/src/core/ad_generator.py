from time import time
from typing import Any, Dict, AsyncIterator
from src.core.base import BaseAdGenerator
from src.models import (
    AdGenerationRequest,
    AdGenerationResponse,
    ProductInfo,
    AdSettings
)
from src.llm.openai_client import OpenAIClient 
from src.prompts.templates import FlexibleAdPromptGenerator
from src.utils.helpers import generate_request_id
     

class AIAdGenerator(BaseAdGenerator):
    """
    AIAdGenerator is responsible for generating advertisements using an LLM client.
    It utilizes a flexible prompt generator to create prompts based on the ad type and tone specified in the request.
    The generator can handle both standard and streaming responses, providing detailed ad content along with product information and settings.
    """

    def __init__(self) -> None:
        """ 
        Initializes the AIAdGenerator with an OpenAI client and a flexible prompt generator.
        """
        self.llm = OpenAIClient()
        self.prompt = FlexibleAdPromptGenerator()

    async def generate(self, request: AdGenerationRequest, **kwargs) -> AdGenerationResponse:
        """
        Generates an advertisement based on the provided request.
        Parameters:
            - request: AdGenerationRequest containing product details and ad settings.
        Returns:
            - AdGenerationResponse with generated ad content and metadata.
        """
        start = time()
        identifier = generate_request_id()

        try:
            system_prompt = self.prompt.generate_prompt(
                ad_type=request.ad_type,
                ad_tone=request.ad_tone,
            )
            product_data = request.model_dump(exclude={"ad_type", "ad_tone"})
            product_str = "\n".join(f"{k}: {v}" for k, v in product_data.items() if v is not None)


            ad_content = await self.llm.generate_text(
                system=system_prompt,
                data_product=product_str,
                max_tokens=1000,
                temperature=1.0,
                **kwargs
            )

            generation_time = time() - start

            return AdGenerationResponse(
                ad_content=ad_content,
                product_info=ProductInfo(
                    product_name=request.product_name,
                    brand=request.brand_name,
                    category=request.category,
                    description=request.description,
                    price=request.price,
                    discounted_price=request.discounted_price,
                    store_link=request.product_url,
                ),
                ad_settings=AdSettings(
                    ad_type=request.ad_type,
                    ad_tone=request.ad_tone,
                ),
                generation_time=generation_time,
                model_used=self.llm.model_name,
                request_id=identifier
            )
        except Exception as e:
            raise Exception(f"Ad generation failed: {str(e)}")
    
    async def generate_streaming(self, request: AdGenerationRequest, **kwargs) -> AsyncIterator[Dict[str, Any]]:
        """
        Generates an advertisement with streaming response based on the provided request.
        Parameters:
            - request: AdGenerationRequest containing product details and ad settings.
        Returns:
            - AsyncIterator yielding chunks of generated ad content and metadata.
        """
        start = time()
        identifier = generate_request_id()

        try:
            yield {
                "status": "processing",
                "message": "Generating your advertisement...",
                "request_id": identifier
            }

            accumulate_content = ""
            product_data = request.model_dump(exclude={"ad_type", "ad_tone"})
            product_str = "\n".join(f"{k}: {v}" for k, v in product_data.items() if v is not None)

            system_prompt = self.prompt.generate_prompt(
                ad_type=request.ad_type,
                ad_tone=request.ad_tone,
            )

            async for chunk in self.llm.generate_text_streaming(
                system=system_prompt,
                data_product=product_str,
                max_tokens=1000,
                temperature=1.0,
                stream=True,
                **kwargs
            ):
                accumulate_content += chunk
                yield {
                    "status": "streaming",
                    "content": chunk,
                    "progress": min(len(accumulate_content) / 500 * 100, 95)  # Rough progress estimate
                } 
            # Final response after streaming is complete
            yield {
                "status": "completed",
                "ad_content": accumulate_content,
                "product_info": {
                    "product_name": request.product_name,
                    "brand": request.brand_name,
                    "category": request.category,
                    "description": request.description,
                    "price": request.price,
                    "discounted_price": request.discounted_price,
                    "store_link": request.product_url,
                },
                "ad_settings": {
                    "ad_type": request.ad_type,
                    "ad_tone": request.ad_tone,
                },
                "generation_time": time() - start,
                "model_used": self.llm.model_name,
                "request_id": identifier
            }
        except Exception as e:
            yield {
                "status": "error",
                "message": str(e),
                "error_code": "generation_failed",
                "request_id": identifier
            }