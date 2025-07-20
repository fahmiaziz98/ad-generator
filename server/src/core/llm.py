from openai import AsyncOpenAI
from config import settings
from typing import Any


class LLM:
    """LLM client for interacting with the Lunos API."""
    def __init__(self) -> None:
        self.client = AsyncOpenAI(
            api_key=settings.LUNOS_API_KEY,
            base_url=settings.lunos_base_url
        )

    async def invoke(self, system: str, data_product: Any):
        """Invoke the LLM with a system prompt and product data."""
        response = await self.client.chat.completions.create(
            model="google/gemma-3-12b-it",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": data_product}
            ],
            temperature=1,
            stream=True
        )
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content