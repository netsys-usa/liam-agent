# LIAM Python SDK

Official Python SDK for the **LIAM Memory Management API**.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🔐 **Secure Authentication** - ECDSA P-256 signature-based authentication
- 🚀 **Async Support** - High-performance async client with aiohttp
- 📦 **Batch Operations** - Create multiple memories concurrently
- 🏷️ **Tag Management** - Organize memories with tags
- 💬 **Chat Integration** - Query memories with natural language

## Installation

```bash
pip install liam-client
```

Or install from source:

```bash
git clone https://github.com/netsys-usa/liam-agent.git
cd liam-python-sdk
pip install -e .
```

## Quick Start

### 1. Generate Key Pair

```python
from liam_client import generate_key_pair, save_key_pair

# Generate and save keys
save_key_pair('private_key.pem', 'public_key.pem')
```

Or via command line:

```bash
python -m liam_client.crypto
```

### 2. Register Your Connector

Use the generated `public_key.pem` to register your connector with the LIAM API. You'll receive an API key.

### 3. Initialize Client

```python
from liam_client import LIAMClient

# Load private key
with open('private_key.pem', 'r') as f:
    private_key = f.read()

# Create client
client = LIAMClient(
    api_key="your-api-key",
    private_key_pem=private_key
)

# Verify connection
health = client.health_check()
print(f"API Status: {health['status']}")
```

### 4. Create & Query Memories

```python
# Create a memory
client.create_memory(
    user_key="user_abc123",
    content="I prefer morning meetings before 10am",
    tag="preferences"
)

# Chat with memory context
response = client.chat(
    user_key="user_abc123",
    query="What time do I prefer for meetings?"
)
print(response['data'])

# List all memories
memories = client.list_memories(user_key="user_abc123")
```

## Async Client

For high-performance applications:

```python
import asyncio
from liam_client import LIAMClientAsync

async def main():
    async with LIAMClientAsync(
        api_key="your-api-key",
        private_key_pem=private_key
    ) as client:
        # Create memories concurrently
        memories = [
            {"content": "Meeting at 3pm", "tag": "calendar"},
            {"content": "Call dentist", "tag": "health"},
            {"content": "Buy groceries", "tag": "shopping"},
        ]
        
        results = await client.create_memories_batch("user_abc123", memories)
        print(f"Created {len(results)} memories")

asyncio.run(main())
```

## API Reference

### Memory Operations

| Method | Description |
|--------|-------------|
| `create_memory(user_key, content, tag?, session_id?)` | Create a new memory |
| `create_memory_with_image(user_key, content, image_base64, tag?)` | Create memory with image |
| `list_memories(user_key, query?, limit?)` | List or search memories |
| `chat(user_key, query, session_id?)` | Chat with memory context |
| `summarize_memory(user_key, memory_id?)` | Get memory summary |
| `forget_memory(user_key, memory_id, permanent?)` | Delete a memory |
| `memory_status(user_key, process_id?)` | Check processing status |

### Tag Operations

| Method | Description |
|--------|-------------|
| `list_tags(user_key)` | List all user tags |
| `add_tag(user_key, memory_id, tag)` | Add tag to memory |
| `get_by_tag(user_key, tag, limit?, offset?)` | Get memories by tag |
| `change_tag(user_key, old_tag, new_tag)` | Rename a tag |

### Utility

| Method | Description |
|--------|-------------|
| `health_check()` | Check API health |

## Examples

See the [examples](./examples) directory for more detailed usage:

- [basic_usage.py](./examples/basic_usage.py) - Getting started
- [async_example.py](./examples/async_example.py) - Async operations
- [batch_operations.py](./examples/batch_operations.py) - Bulk memory creation

## Configuration

### Environment Variables

```bash
export LIAM_API_KEY="your-api-key"
export LIAM_PRIVATE_KEY_PATH="/path/to/private_key.pem"
```

```python
import os
from liam_client import LIAMClient

client = LIAMClient.from_env()  # Reads from environment variables
```

### Custom Base URL

```python
client = LIAMClient(
    api_key="your-api-key",
    private_key_pem=private_key,
    base_url="https://custom-api.example.com/api"
)
```

## Security Best Practices

1. **Never commit private keys** - Add `*.pem` to `.gitignore`
2. **Use environment variables** - Store credentials securely
3. **Server-side only** - Never expose private keys to client-side code
4. **Rotate keys regularly** - Generate new key pairs periodically

## Development

### Setup

```bash
git clone https://github.com/anthropic-ai/liam-python-sdk.git
cd liam-python-sdk
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/
```

### Code Style

```bash
black liam_client/
flake8 liam_client/
```

## Requirements

- Python 3.8+
- cryptography >= 41.0.0
- requests >= 2.28.0
- aiohttp >= 3.8.0 (for async client)

## Documentation

Full API documentation: [https://web.askbuddy.ai/brain/#/developers](https://web.askbuddy.ai/brain/#/developers)

## Support

- 📧 Email: support@netxd.com
- 📖 Docs: [API Documentation](https://web.askbuddy.ai/brain/#/developers)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0 (2025-01-XX)
- Initial release
- Sync and async clients
- Full API coverage
- Key generation utilities
