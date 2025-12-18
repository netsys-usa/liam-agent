#!/usr/bin/env python3
"""
XDB API Client - Basic Usage Example

This example demonstrates the fundamental operations of the XDB client:
- Creating memories
- Listing and searching memories
- Chatting with memory context
- Working with tags

Before running:
1. Generate keys: python -m xdb_client.crypto
2. Register your connector with the public key to get an API key
3. Update the configuration below
"""

from xdb_client import XDBClient

# =============================================================================
# Configuration - UPDATE THESE VALUES
# =============================================================================

API_KEY = "your-api-key-here"
PRIVATE_KEY_PATH = "private_key.pem"
USER_KEY = "example_user_123"  # Your user's unique identifier

# =============================================================================
# Initialize Client
# =============================================================================

def get_client() -> XDBClient:
    """Create and return the XDB client."""
    with open(PRIVATE_KEY_PATH, 'r') as f:
        private_key = f.read()
    
    return XDBClient(
        api_key=API_KEY,
        private_key_pem=private_key
    )


# =============================================================================
# Examples
# =============================================================================

def example_health_check():
    """Verify API connection."""
    print("\n" + "=" * 50)
    print("🏥 Health Check")
    print("=" * 50)
    
    client = get_client()
    result = client.health_check()
    
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message', 'OK')}")
    
    return result.get('status') == 'Success'


def example_create_memories():
    """Create some example memories."""
    print("\n" + "=" * 50)
    print("📝 Creating Memories")
    print("=" * 50)
    
    client = get_client()
    
    memories = [
        ("I prefer morning meetings before 10am", "preferences"),
        ("My favorite coffee is a flat white with oat milk", "preferences"),
        ("Project deadline is next Friday", "work"),
        ("Doctor appointment on Monday at 2pm", "health"),
        ("Need to buy: milk, eggs, bread, cheese", "shopping"),
    ]
    
    for content, tag in memories:
        result = client.create_memory(
            user_key=USER_KEY,
            content=content,
            tag=tag
        )
        status = "✓" if result.get('status') == 'Success' else "✗"
        print(f"  {status} [{tag}] {content[:40]}...")
    
    print(f"\nCreated {len(memories)} memories")


def example_list_memories():
    """List all memories for the user."""
    print("\n" + "=" * 50)
    print("📋 Listing Memories")
    print("=" * 50)
    
    client = get_client()
    result = client.list_memories(user_key=USER_KEY, limit=10)
    
    print(f"Status: {result.get('status')}")
    
    if result.get('data'):
        print(f"Found {len(result['data'])} memories:")
        for i, memory in enumerate(result['data'], 1):
            print(f"  {i}. {memory}")
    else:
        print("No memories found")


def example_search_memories():
    """Search memories with a query."""
    print("\n" + "=" * 50)
    print("🔍 Searching Memories")
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


def example_chat():
    """Chat with memory context."""
    print("\n" + "=" * 50)
    print("💬 Chat with Memory")
    print("=" * 50)
    
    client = get_client()
    
    questions = [
        "What time do I prefer for meetings?",
        "What kind of coffee do I like?",
        "When is my doctor appointment?",
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        result = client.chat(
            user_key=USER_KEY,
            query=question
        )
        print(f"A: {result.get('data', 'No response')}")


def example_tags():
    """Work with tags."""
    print("\n" + "=" * 50)
    print("🏷️ Tag Operations")
    print("=" * 50)
    
    client = get_client()
    
    # List all tags
    result = client.list_tags(user_key=USER_KEY)
    print(f"All tags: {result.get('data', [])}")
    
    # Get memories by tag
    result = client.get_by_tag(user_key=USER_KEY, tag="preferences")
    count = len(result.get('data', []))
    print(f"Memories with 'preferences' tag: {count}")


def example_summarize():
    """Get a summary of memories."""
    print("\n" + "=" * 50)
    print("📊 Summarize Memories")
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
    print("🚀 XDB API Client - Basic Usage Examples")
    print("=" * 60)
    
    try:
        # Check connection first
        if not example_health_check():
            print("\n❌ API health check failed. Check your configuration.")
            return
        
        # Run examples
        example_create_memories()
        example_list_memories()
        example_search_memories()
        example_chat()
        example_tags()
        example_summarize()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except FileNotFoundError:
        print("\n❌ Error: Private key file not found!")
        print("Run 'python -m xdb_client.crypto' to generate keys.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you've updated API_KEY and USER_KEY in this file.")


if __name__ == "__main__":
    main()
