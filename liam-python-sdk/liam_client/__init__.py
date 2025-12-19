"""
LIAM Python SDK

Official Python client for the LIAM Memory Management API.

Basic Usage:
    from liam_client import LIAMClient
    
    client = LIAMClient(api_key="your-api-key")
    
    result = client.create_memory(
        user_key="user_hash",
        content="Remember this",
        tag="notes"
    )

Async Usage:
    from liam_client import LIAMClientAsync
    
    async with LIAMClientAsync(api_key="your-key") as client:
        result = await client.create_memory(...)

Environment Variables:
    from liam_client import LIAMClient
    
    # Uses LIAM_API_KEY environment variable
    client = LIAMClient.from_env()
"""

__version__ = "1.0.0"
__author__ = "NetXD"
__email__ = "support@netxd.com"

from .client import LIAMClient, LIAMClientError, LIAMAPIError

# Async client is optional (requires aiohttp)
try:
    from .async_client import LIAMClientAsync
except ImportError:
    LIAMClientAsync = None  # aiohttp not installed

__all__ = [
    "LIAMClient",
    "LIAMClientAsync",
    "LIAMClientError",
    "LIAMAPIError",
    "__version__",
]
