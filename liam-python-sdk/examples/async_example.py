#!/usr/bin/env python3
"""
LIAM API Client - Async Usage Example

This example demonstrates high-performance async operations:
- Concurrent memory creation
- Batch operations
- Connection pooling with context manager

Requires: pip install aiohttp

Before running:
1. Generate keys: python -m liam_client.crypto
2. Register your connector with the public key to get an API key
3. Update the configuration below
"""

import asyncio
import time
from typing import List, Dict

from liam_client import LIAMClientAsync

# =============================================================================
# Configuration - UPDATE THESE VALUES
# =============================================================================

API_KEY = "your-api-key-here"
PRIVATE_KEY_PATH = "private_key.pem"
USER_KEY = "example_user_123"

# =============================================================================
# Helper Functions
# =============================================================================

def load_private_key() -> str:
    """Load private key from file."""
    with open(PRIVATE_KEY_PATH, 'r') as f:
        return f.read()


# =============================================================================
# Examples
# =============================================================================

async def example_basic_async():
    """Basic async operations."""
    print("\n" + "=" * 50)
    print("🚀 Basic Async Operations")
    print("=" * 50)
    
    private_key = load_private_key()
    
    # Use context manager for connection pooling
    async with LIAMClientAsync(
        api_key=API_KEY,
        private_key_pem=private_key
    ) as client:
        # Health check
        health = await client.health_check()
        print(f"API Status: {health.get('status')}")
        
        # Create a memory
        result = await client.create_memory(
            user_key=USER_KEY,
            content="Async memory creation test",
            tag="async-test"
        )
        print(f"Created memory: {result.get('status')}")
        
        # List memories
        memories = await client.list_memories(user_key=USER_KEY, limit=5)
        print(f"Listed {len(memories.get('data', []))} memories")


async def example_concurrent_creation():
    """Create multiple memories concurrently."""
    print("\n" + "=" * 50)
    print("⚡ Concurrent Memory Creation")
    print("=" * 50)
    
    private_key = load_private_key()
    
    memories = [
        {"content": "Meeting notes from Monday standup", "tag": "work"},
        {"content": "Grocery list: apples, bananas, oranges", "tag": "shopping"},
        {"content": "Book recommendation: The Pragmatic Programmer", "tag": "reading"},
        {"content": "Gym workout: 30 min cardio, 20 min weights", "tag": "health"},
        {"content": "Birthday gift ideas for mom", "tag": "personal"},
        {"content": "Python async/await patterns learned today", "tag": "learning"},
        {"content": "Recipe: homemade pasta with tomato sauce", "tag": "cooking"},
        {"content": "Movie to watch: Inception", "tag": "entertainment"},
        {"content": "Project milestone: complete API integration", "tag": "work"},
        {"content": "Vacation ideas: Japan, Iceland, New Zealand", "tag": "travel"},
    ]
    
    async with LIAMClientAsync(
        api_key=API_KEY,
        private_key_pem=private_key
    ) as client:
        print(f"Creating {len(memories)} memories concurrently...")
        
        start_time = time.time()
        
        # Use batch operation
        results = await client.create_memories_batch(USER_KEY, memories)
        
        elapsed = time.time() - start_time
        
        # Count successes
        success_count = sum(
            1 for r in results 
            if isinstance(r, dict) and r.get('status') == 'Success'
        )
        
        print(f"✓ Created {success_count}/{len(memories)} memories")
        print(f"⏱ Time: {elapsed:.2f} seconds")
        print(f"📊 Rate: {len(memories)/elapsed:.1f} memories/second")


async def example_parallel_tag_fetch():
    """Fetch memories from multiple tags in parallel."""
    print("\n" + "=" * 50)
    print("🏷️ Parallel Tag Fetching")
    print("=" * 50)
    
    private_key = load_private_key()
    
    tags = ["work", "personal", "health", "shopping", "learning"]
    
    async with LIAMClientAsync(
        api_key=API_KEY,
        private_key_pem=private_key
    ) as client:
        print(f"Fetching memories for {len(tags)} tags in parallel...")
        
        start_time = time.time()
        
        # Fetch all tags concurrently
        results = await client.get_all_tagged_memories(USER_KEY, tags)
        
        elapsed = time.time() - start_time
        
        print(f"\nResults (fetched in {elapsed:.2f}s):")
        for tag, result in results.items():
            if isinstance(result, dict):
                count = len(result.get('data', []))
                print(f"  {tag}: {count} memories")
            else:
                print(f"  {tag}: Error - {result}")


async def example_high_throughput():
    """High-throughput batch operations with rate limiting."""
    print("\n" + "=" * 50)
    print("🔥 High Throughput Example")
    print("=" * 50)
    
    private_key = load_private_key()
    
    # Generate test memories
    total_count = 50
    batch_size = 10
    
    async with LIAMClientAsync(
        api_key=API_KEY,
        private_key_pem=private_key
    ) as client:
        print(f"Creating {total_count} memories in batches of {batch_size}...")
        
        start_time = time.time()
        total_created = 0
        
        for batch_num in range(0, total_count, batch_size):
            # Create batch
            memories = [
                {
                    "content": f"High-throughput test memory #{i}",
                    "tag": f"batch-{batch_num // batch_size}"
                }
                for i in range(batch_num, min(batch_num + batch_size, total_count))
            ]
            
            results = await client.create_memories_batch(
                USER_KEY, 
                memories,
                concurrency=batch_size  # Limit concurrent requests
            )
            
            success_count = sum(
                1 for r in results 
                if isinstance(r, dict) and r.get('status') == 'Success'
            )
            total_created += success_count
            
            print(f"  Batch {batch_num // batch_size + 1}: {success_count}/{len(memories)}")
            
            # Small delay between batches to avoid rate limiting
            await asyncio.sleep(0.1)
        
        elapsed = time.time() - start_time
        
        print(f"\n✓ Total created: {total_created}/{total_count}")
        print(f"⏱ Total time: {elapsed:.2f} seconds")
        print(f"📊 Throughput: {total_count/elapsed:.1f} memories/second")


# =============================================================================
# Main
# =============================================================================

async def main():
    """Run all async examples."""
    print("\n" + "=" * 60)
    print("🚀 LIAM API Client - Async Examples")
    print("=" * 60)
    
    try:
        await example_basic_async()
        await example_concurrent_creation()
        await example_parallel_tag_fetch()
        await example_high_throughput()
        
        print("\n" + "=" * 60)
        print("✅ All async examples completed!")
        print("=" * 60)
        
    except FileNotFoundError:
        print("\n❌ Error: Private key file not found!")
        print("Run 'python -m liam_client.crypto' to generate keys.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you've updated API_KEY and USER_KEY.")


if __name__ == "__main__":
    asyncio.run(main())
