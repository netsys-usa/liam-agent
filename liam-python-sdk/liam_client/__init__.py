"""
XDB Python SDK

Official Python client for the LIAM XDB Memory Management API.

Basic Usage:
    from xdb_client import XDBClient
    
    client = XDBClient(
        api_key="your-api-key",
        private_key_pem=open('private_key.pem').read()
    )
    
    result = client.create_memory(
        user_key="user_hash",
        content="Remember this",
        tag="notes"
    )

Async Usage:
    from xdb_client import XDBClientAsync
    
    async with XDBClientAsync(api_key, private_key) as client:
        result = await client.create_memory(...)

Key Generation:
    from xdb_client import generate_key_pair, save_key_pair
    
    private_pem, public_pem = generate_key_pair()
    save_key_pair('private.pem', 'public.pem')
"""

__version__ = "1.0.0"
__author__ = "NetXD"
__email__ = "support@netxd.com"

from .client import XDBClient
from .crypto import generate_key_pair, save_key_pair

# Async client is optional (requires aiohttp)
try:
    from .async_client import XDBClientAsync
except ImportError:
    XDBClientAsync = None  # aiohttp not installed

__all__ = [
    "XDBClient",
    "XDBClientAsync",
    "generate_key_pair",
    "save_key_pair",
    "__version__",
]
