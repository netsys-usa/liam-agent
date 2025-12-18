#!/usr/bin/env python3
"""
LIAM API Client - Batch Operations Example

This example shows how to efficiently handle bulk operations:
- Importing memories from files
- Bulk tagging operations
- Exporting and backup

Before running:
1. Generate keys: python -m liam_client.crypto
2. Register your connector with the public key
3. Update the configuration below
"""

import json
import csv
import asyncio
from pathlib import Path
from typing import List, Dict

from liam_client import LIAMClient

# Try to import async client
try:
    from liam_client import LIAMClientAsync
    HAS_ASYNC = True
except ImportError:
    HAS_ASYNC = False

# =============================================================================
# Configuration - UPDATE THESE VALUES
# =============================================================================

API_KEY = "your-api-key-here"
PRIVATE_KEY_PATH = "private_key.pem"
USER_KEY = "example_user_123"

# =============================================================================
# Sync Batch Operations
# =============================================================================

def import_from_json(file_path: str, user_key: str) -> List[Dict]:
    """
    Import memories from a JSON file.
    
    Expected JSON format:
    [
        {"content": "Memory text", "tag": "optional-tag"},
        ...
    ]
    """
    print(f"\n📥 Importing from {file_path}...")
    
    with open(file_path, 'r') as f:
        memories = json.load(f)
    
    with open(PRIVATE_KEY_PATH, 'r') as f:
        private_key = f.read()
    
    client = LIAMClient(api_key=API_KEY, private_key_pem=private_key)
    
    results = []
    for i, memory in enumerate(memories):
        result = client.create_memory(
            user_key=user_key,
            content=memory['content'],
            tag=memory.get('tag')
        )
        results.append(result)
        
        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(memories)}")
    
    success_count = sum(1 for r in results if r.get('status') == 'Success')
    print(f"✓ Imported {success_count}/{len(memories)} memories")
    
    return results


def import_from_csv(file_path: str, user_key: str) -> List[Dict]:
    """
    Import memories from a CSV file.
    
    Expected CSV format:
    content,tag
    "Memory text","optional-tag"
    ...
    """
    print(f"\n📥 Importing from {file_path}...")
    
    memories = []
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            memories.append({
                'content': row['content'],
                'tag': row.get('tag', '').strip() or None
            })
    
    with open(PRIVATE_KEY_PATH, 'r') as f:
        private_key = f.read()
    
    client = LIAMClient(api_key=API_KEY, private_key_pem=private_key)
    
    results = []
    for i, memory in enumerate(memories):
        result = client.create_memory(
            user_key=user_key,
            content=memory['content'],
            tag=memory['tag']
        )
        results.append(result)
        
        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(memories)}")
    
    success_count = sum(1 for r in results if r.get('status') == 'Success')
    print(f"✓ Imported {success_count}/{len(memories)} memories")
    
    return results


def export_to_json(user_key: str, output_path: str) -> int:
    """Export all memories to a JSON file."""
    print(f"\n📤 Exporting to {output_path}...")
    
    with open(PRIVATE_KEY_PATH, 'r') as f:
        private_key = f.read()
    
    client = LIAMClient(api_key=API_KEY, private_key_pem=private_key)
    
    result = client.list_memories(user_key=user_key, limit=1000)
    memories = result.get('data', [])
    
    with open(output_path, 'w') as f:
        json.dump(memories, f, indent=2)
    
    print(f"✓ Exported {len(memories)} memories")
    return len(memories)


def bulk_change_tag(user_key: str, old_tag: str, new_tag: str) -> Dict:
    """Change tag for all memories with a specific tag."""
    print(f"\n🏷️ Changing tag: {old_tag} → {new_tag}")
    
    with open(PRIVATE_KEY_PATH, 'r') as f:
        private_key = f.read()
    
    client = LIAMClient(api_key=API_KEY, private_key_pem=private_key)
    
    result = client.change_tag(
        user_key=user_key,
        old_tag=old_tag,
        new_tag=new_tag
    )
    
    print(f"✓ Status: {result.get('status')}")
    return result


# =============================================================================
# Async Batch Operations (if aiohttp is installed)
# =============================================================================

if HAS_ASYNC:
    async def import_from_json_async(file_path: str, user_key: str) -> List[Dict]:
        """
        Import memories from JSON file using async for better performance.
        """
        print(f"\n📥 Importing from {file_path} (async)...")
        
        with open(file_path, 'r') as f:
            memories = json.load(f)
        
        with open(PRIVATE_KEY_PATH, 'r') as f:
            private_key = f.read()
        
        async with LIAMClientAsync(api_key=API_KEY, private_key_pem=private_key) as client:
            # Convert to batch format
            batch = [
                {"content": m['content'], "tag": m.get('tag')}
                for m in memories
            ]
            
            results = await client.create_memories_batch(user_key, batch)
        
        success_count = sum(
            1 for r in results 
            if isinstance(r, dict) and r.get('status') == 'Success'
        )
        print(f"✓ Imported {success_count}/{len(memories)} memories")
        
        return results


# =============================================================================
# Sample Data Generation
# =============================================================================

def create_sample_json(output_path: str = "sample_memories.json"):
    """Create a sample JSON file for testing imports."""
    sample_data = [
        {"content": "Meeting with client at 3pm on Tuesday", "tag": "work"},
        {"content": "Buy birthday present for Sarah", "tag": "personal"},
        {"content": "Python project deadline is Friday", "tag": "work"},
        {"content": "Dentist appointment next Monday", "tag": "health"},
        {"content": "Favorite restaurant: Italian place on Main St", "tag": "food"},
        {"content": "Book to read: Atomic Habits", "tag": "reading"},
        {"content": "Gym schedule: Mon, Wed, Fri mornings", "tag": "health"},
        {"content": "Anniversary is June 15th", "tag": "personal"},
        {"content": "Car service due in 2 weeks", "tag": "errands"},
        {"content": "New recipe: chicken stir fry", "tag": "food"},
    ]
    
    with open(output_path, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print(f"✓ Created sample file: {output_path}")
    return output_path


def create_sample_csv(output_path: str = "sample_memories.csv"):
    """Create a sample CSV file for testing imports."""
    sample_data = [
        ("Meeting with client at 3pm on Tuesday", "work"),
        ("Buy birthday present for Sarah", "personal"),
        ("Python project deadline is Friday", "work"),
        ("Dentist appointment next Monday", "health"),
        ("Favorite restaurant: Italian place on Main St", "food"),
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['content', 'tag'])
        writer.writerows(sample_data)
    
    print(f"✓ Created sample file: {output_path}")
    return output_path


# =============================================================================
# Main
# =============================================================================

def main():
    """Demonstrate batch operations."""
    print("\n" + "=" * 60)
    print("🔄 LIAM API Client - Batch Operations")
    print("=" * 60)
    
    print("\nAvailable operations:")
    print("1. Create sample JSON file")
    print("2. Create sample CSV file")
    print("3. Import from JSON")
    print("4. Import from CSV")
    print("5. Export to JSON")
    print("6. Bulk change tag")
    if HAS_ASYNC:
        print("7. Import from JSON (async - faster)")
    print("0. Exit")
    
    while True:
        choice = input("\nSelect operation (0-7): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            create_sample_json()
        elif choice == '2':
            create_sample_csv()
        elif choice == '3':
            path = input("JSON file path [sample_memories.json]: ").strip()
            import_from_json(path or "sample_memories.json", USER_KEY)
        elif choice == '4':
            path = input("CSV file path [sample_memories.csv]: ").strip()
            import_from_csv(path or "sample_memories.csv", USER_KEY)
        elif choice == '5':
            path = input("Output path [exported_memories.json]: ").strip()
            export_to_json(USER_KEY, path or "exported_memories.json")
        elif choice == '6':
            old_tag = input("Old tag: ").strip()
            new_tag = input("New tag: ").strip()
            if old_tag and new_tag:
                bulk_change_tag(USER_KEY, old_tag, new_tag)
        elif choice == '7' and HAS_ASYNC:
            path = input("JSON file path [sample_memories.json]: ").strip()
            asyncio.run(import_from_json_async(path or "sample_memories.json", USER_KEY))
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
