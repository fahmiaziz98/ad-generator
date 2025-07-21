from ..models.ad import AdType, AdTone
from ..core.llm import LLM
from ..core.prompt_templates import FlexibleAdPromptGenerator


class AdGenerator:
    """Ad Generator for creating ads using LLM."""
    def __init__(self) -> None:
        self.template = FlexibleAdPromptGenerator()
        self.llm = LLM()

    def generate(self, data_product: str, ad_type: AdType, ad_tone: AdTone):
        """Generate ad content based on product data, ad type, and ad tone."""
        if not isinstance(ad_type, AdType):
            raise ValueError(f"Invalid ad type: {ad_type}")
        if not isinstance(ad_tone, AdTone):
            raise ValueError(f"Invalid ad tone: {ad_tone}")
        if not isinstance(data_product, str):
            raise ValueError("data_product must be a string")
        prompt = self.template.generate_prompt(ad_type, ad_tone)

        return self.llm.invoke(prompt, data_product)
        
