# LIAM Python SDK

Official Python SDK for the **LIAM Memory Management API**.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🚀 **Simple API** - Easy to use with just an API key
- ⚡ **Async Support** - High-performance async client with aiohttp
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
cd liam-agent/liam-python-sdk
pip install -e .
```

## Quick Start

### 1. Get Your API Key

Sign in to LIAM and get your API key from the dashboard.

### 2. Initialize Client

```python
from liam_client import LIAMClient

client = LIAMClient(api_key="your-api-key")

# Verify connection
health = client.health_check()
print(f"API Status: {health['status']}")
```

### 3. Create & Query Memories

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
    async with LIAMClientAsync(api_key="your-api-key") as client:
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

## Configuration

### Environment Variables

```bash
export LIAM_API_KEY="your-api-key"
```

```python
from liam_client import LIAMClient

client = LIAMClient.from_env()  # Reads LIAM_API_KEY from environment
```

### Custom Base URL

```python
client = LIAMClient(
    api_key="your-api-key",
    base_url="https://custom-api.example.com/api"
)
```

## Requirements

- Python 3.8+
- requests >= 2.28.0
- aiohttp >= 3.8.0 (for async client)

## Documentation

Full API documentation: [https://liam.netxd.com/#/developers](https://liam.netxd.com/#/developers)

## Support

- 📧 Email: support@netxd.com
- 📖 Docs: [API Documentation](https://liam.netxd.com/#/developers)
- 🐛 Issues: [GitHub Issues](https://github.com/netsys-usa/liam-agent/issues)

## License

MIT License - see [LICENSE](LICENSE) file for details.
