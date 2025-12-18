"""
LIAM Python SDK

Official Python client for the LIAM Memory Management API.

Basic Usage:
    from liam_client import LIAMClient
    
    client = LIAMClient(
        api_key="your-api-key",
        private_key_pem=open('private_key.pem').read()
    )
    
    result = client.create_memory(
        user_key="user_hash",
        content="Remember this",
        tag="notes"
    )

Async Usage:
    from liam_client import LIAMClientAsync
    
    async with LIAMClientAsync(api_key, private_key) as client:
        result = await client.create_memory(...)

Key Generation:
    from liam_client import generate_key_pair, save_key_pair
    
    private_pem, public_pem = generate_key_pair()
    save_key_pair('private.pem', 'public.pem')
"""

__version__ = "1.0.0"
__author__ = "NetXD"
__email__ = "support@netxd.com"

from .client import LIAMClient
from .crypto import generate_key_pair, save_key_pair

# Async client is optional (requires aiohttp)
try:
    from .async_client import LIAMClientAsync
except ImportError:
    LIAMClientAsync = None  # aiohttp not installed

__all__ = [
    "LIAMClient",
    "LIAMClientAsync",
    "generate_key_pair",
    "save_key_pair",
    "__version__",
]
