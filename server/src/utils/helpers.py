import uuid

def generate_request_id() -> str:
    """Generate a unique request ID for tracking"""
    return str(uuid.uuid4())