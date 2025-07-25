from fastapi import HTTPException, Header
from src.config import settings
from starlette.status import HTTP_403_FORBIDDEN
from time import time

# In-memory rate limiter storage
_rate_limiter_storage = {}

def get_rate_limiter(client_id: str = Header(...)) -> None:
    """
    Rate limiter middleware to restrict API usage per client.
    """
    global _rate_limiter_storage
    current_time = time()
    window_start = current_time - settings.RATE_LIMIT_WINDOW

    if client_id not in _rate_limiter_storage:
        _rate_limiter_storage[client_id] = []

    # Remove outdated requests
    _rate_limiter_storage[client_id] = [
        timestamp for timestamp in _rate_limiter_storage[client_id]
        if timestamp > window_start
    ]

    # Check if the client exceeds the rate limit
    if len(_rate_limiter_storage[client_id]) >= settings.RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Rate limit exceeded. Please try again later."
        )

    # Record the current request
    _rate_limiter_storage[client_id].append(current_time)
