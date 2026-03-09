# LIAM Python SDK

Official Python SDK for the **LIAM Memory Management API**.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🔐 **Secure Authentication** - ECDSA signature-based API authentication
- ⚡ **Async Support** - High-performance async client with aiohttp
- 📦 **Batch Operations** - Create multiple memories concurrently
- 🏷️ **Tag Management** - Organize memories with tags
- 💬 **Chat Integration** - Query memories with natural language

---

## Installation

### From PyPI

```bash
pip install liam-client
```

### From Source (Latest / Development)

```bash
git clone https://github.com/netsys-usa/liam-agent.git
cd liam-agent/liam-python-sdk
pip install -e .
```

---

## Getting Started

### Step 1 — Create Your Account

Sign up at **[https://web.askbuddy.ai/brain/#/login](https://web.askbuddy.ai/brain/#/login)**

After registration, a default workspace will be created automatically for you.

---

### Step 2 — Get Your API Key

1. Log in and navigate to **Workspaces** in the left sidebar
2. You'll see your workspace listed with a masked **API Key** (e.g., `M7a*****QI2Q`)
3. Click the **Copy** icon next to your API Key to copy it

> Your workspace also shows its **Status** (must be `ACTIVATED`) and the **Institution Id** assigned to it.

---

### Step 3 — Generate Your Private Key

The LIAM API uses **ECDSA key-pair authentication**. You need to generate a key pair and register the public key.

1. Click on your workspace name to open the workspace detail page
2. Scroll down to the **Key Pair(s)** section
3. Click **"Generate New Key"**
4. Copy and securely store the **Private Key** that is returned — it will only be shown once

> ⚠️ **Keep your private key secret.** Never commit it to version control or share it publicly.

---

### Step 4 — Add an LLM Key

LIAM uses an LLM to power memory chat and summarization. You must connect at least one LLM key.

1. On the workspace detail page, scroll down to the **LLM Keys** section
2. Click **"Add New Key"** (top right of the section)
3. Enter your LLM provider API key (e.g., OpenAI) along with the **Identifier** and **Model Name**
4. Save — the key status will update to **Active**

---

### Step 5 — Initialize the Client

```python
from liam_client import LIAMClient

client = LIAMClient(
    api_key="your-api-key",          # Copied from Workspaces page
    private_key="your-base64-encoded-private-key"  # Generated in Step 3
)

# Verify connection
health = client.health_check()
print(f"API Status: {health['status']}")
```

---

## Quick Examples

### Create & Query Memories

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

---

## Async Client

For high-performance applications:

```python
import asyncio
from liam_client import LIAMClientAsync

async def main():
    async with LIAMClientAsync(
        api_key="your-api-key",
        private_key="your-base64-encoded-private-key"
    ) as client:
        memories = [
            {"content": "Meeting at 3pm", "tag": "calendar"},
            {"content": "Call dentist", "tag": "health"},
            {"content": "Buy groceries", "tag": "shopping"},
        ]
        
        results = await client.create_memories_batch("user_abc123", memories)
        print(f"Created {len(results)} memories")

asyncio.run(main())
```

---

## Configuration

### Environment Variables

```bash
export LIAM_API_KEY="your-api-key"
export LIAM_PRIVATE_KEY_PATH="/path/to/private_key.pem"
# Or use LIAM_PRIVATE_KEY for the key content directly
```

```python
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

---

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

---

## Examples

See the [examples](./examples) directory for more detailed usage:

- [basic_usage.py](./examples/basic_usage.py) - Getting started
- [async_example.py](./examples/async_example.py) - Async operations

---

## Requirements

- Python 3.8+
- requests >= 2.28.0
- cryptography >= 41.0.0
- aiohttp >= 3.8.0 (for async client)

---

## Documentation

Full API documentation: [https://web.askbuddy.ai/brain/#/developers](https://web.askbuddy.ai/brain/#/developers)

---

## Support

- 📧 Email: support@netxd.com
- 📖 Docs: [API Documentation](https://web.askbuddy.ai/brain/#/developers)
- 🐛 Issues: [GitHub Issues](https://github.com/netsys-usa/liam-agent/issues)

---

## License

MIT License - see [LICENSE](LICENSE) file for details.