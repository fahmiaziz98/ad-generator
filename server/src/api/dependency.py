from functools import lru_cache
from core.ad_generator import AdGenerator

@lru_cache()
def get_ad_generator() -> AdGenerator:
    """
    Create and return a singleton instance of AdGenerator.
    This function uses lru_cache to ensure that only one instance is created.
    """
    return AdGenerator()