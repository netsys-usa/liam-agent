"""
LIAM Python SDK

Official Python client for the LIAM Memory Management API.

Basic Usage:
    from liam_client import LIAMClient
    
    client = LIAMClient(
        api_key="your-api-key",
        private_key="your-base64-encoded-private-key"
    )
    
    result = client.create_memory(
        user_key="user_hash",
        content="Remember this",
        tag="notes"
    )

Async Usage:
    from liam_client import LIAMClientAsync
    
    async with LIAMClientAsync(
        api_key="your-key",
        private_key="base64-key"
    ) as client:
        result = await client.create_memory(...)

Environment Variables:
    from liam_client import LIAMClient
    
    # Uses LIAM_API_KEY and LIAM_PRIVATE_KEY environment variables
    client = LIAMClient.from_env()
"""

__version__ = "1.0.0"
__author__ = "NetXD"
__email__ = "support@netxd.com"

from .client import LIAMClient, LIAMClientError, LIAMAuthenticationError, LIAMAPIError

# Async client is optional (requires aiohttp)
try:
    from .async_client import LIAMClientAsync
except ImportError:
    LIAMClientAsync = None  # aiohttp not installed

__all__ = [
    "LIAMClient",
    "LIAMClientAsync",
    "LIAMClientError",
    "LIAMAuthenticationError",
    "LIAMAPIError",
    "__version__",
]
