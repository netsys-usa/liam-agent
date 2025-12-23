#!/usr/bin/env python3
"""
LIAM API Client - Basic Usage Example

This example demonstrates the fundamental operations of the LIAM client:
- Creating memories
- Listing and searching memories
- Chatting with memory context
- Working with tags

Before running:
1. Get your API key from the LIAM dashboard
2. Get your private key (PEM format)
3. Update the configuration below
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import liam_client without installing
sys.path.insert(0, str(Path(__file__).parent.parent))

from liam_client import LIAMClient

# =============================================================================
# Configuration - UPDATE THESE VALUES
# =============================================================================

API_KEY = "api-key"
USER_KEY = "user-key"  # Your user's unique identifier

# Option 1: Load from file
PRIVATE_KEY_PATH = "private-key.pem"
with open(PRIVATE_KEY_PATH, 'r') as f:
    PRIVATE_KEY = f.read()

# Option 2: Paste your PEM key directly (keep the triple quotes)
# PRIVATE_KEY = """-----BEGIN EC PRIVATE KEY-----
# MHQCAQEEIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx==
# -----END EC PRIVATE KEY-----"""

# =============================================================================
# Initialize Client
# =============================================================================

def get_client() -> LIAMClient:
    """Create and return the LIAM client."""
    return LIAMClient(api_key=API_KEY, private_key=PRIVATE_KEY)


# =============================================================================
# Examples
# =============================================================================

def example_health_check():
    """Verify API connection."""
    print("\n" + "=" * 50)
    print("Health Check")
    print("=" * 50)
    
    client = get_client()
    result = client.health_check()
    
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message', 'OK')}")
    
    return result.get('status') == 'Success'


def example_create_memories():
    """Create some example memories."""
    print("\n" + "=" * 50)
    print("Creating Memories")
    print("=" * 50)
    
    client = get_client()
    
    memories = [
        ("I prefer morning meetings before 10am", "FOOD_PREFERENCES"),
        ("My favorite coffee is a flat white with oat milk", "FOOD_PREFERENCES"),
        ("Project deadline is next Friday", "WORK"),
        ("Doctor appointment on Monday at 2pm", "HEALTH"),
        ("Need to buy: milk, eggs, bread, cheese", "SHOPPING"),
    ]
    
    for content, tag in memories:
        result = client.create_memory(
            user_key=USER_KEY,
            content=content,
            tag=tag
        )
        status = "[OK]" if result.get('status') == 'Success' else "[FAIL]"
        print(f"  {status} [{tag}] {content[:40]}...")
    
    print(f"\nCreated {len(memories)} memories")


def example_list_memories():
    """List all memories for the user."""
    print("\n" + "=" * 50)
    print("Listing Memories")
    print("=" * 50)
    
    client = get_client()
    result = client.list_memories(user_key=USER_KEY, limit=10)
    
    print(f"Status: {result.get('status')}")    
    if result.get('data'):
        print(f"Found {len(result['data']['memories'])} memories:")
        for i, memory in enumerate(result['data']['memories'], 1):
            print(f"  {i}. {memory['memory']}")
    else:
        print("No memories found")


def example_search_memories():
    """Search memories with a query."""
    print("\n" + "=" * 50)
    print("Searching Memories")
    print("=" * 50)
    
    client = get_client()
    
    queries = ["coffee", "meeting", "deadline"]
    
    for query in queries:
        result = client.list_memories(
            user_key=USER_KEY,
            query=query,
            limit=5
        )
        count = len(result.get('data', []))
        print(f"  '{query}': {count} results")


def example_tags():
    """Work with tags."""
    print("\n" + "=" * 50)
    print("Tag Operations")
    print("=" * 50)
    
    client = get_client()
    
    # List all tags
    result = client.list_tags(user_key=USER_KEY)
    print(f"All tags: {result.get('data', [])}")
    
    # Get memories by tag
    result = client.get_by_tag(user_key=USER_KEY, tag="FOOD_PREFERENCES")
    
    data = result.get('data', [])    
    
    count = len(data['memories'])
    print(f"Memories with 'preferences' tag: {count}")


def example_summarize():
    """Get a summary of memories."""
    print("\n" + "=" * 50)
    print("Summarize Memories")
    print("=" * 50)
    
    client = get_client()
    result = client.summarize_memory(user_key=USER_KEY)
    
    print(f"Summary: {result.get('data', 'No summary available')}")


# =============================================================================
# Main
# =============================================================================

def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("LIAM API Client - Basic Usage Examples")
    print("=" * 60)
    
    try:
        # Check connection first
        if not example_health_check():
            print("\n[ERROR] API health check failed. Check your configuration.")
            return
        
        # Run examples
        example_create_memories()
        example_list_memories()
        example_search_memories()
        example_tags()
        
        print("\n" + "=" * 60)
        print("[SUCCESS] All examples completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nMake sure you've configured:")
        print("  - API_KEY: Your API key from LIAM dashboard")
        print("  - PRIVATE_KEY: Your PEM-formatted private key")


if __name__ == "__main__":
    main()
