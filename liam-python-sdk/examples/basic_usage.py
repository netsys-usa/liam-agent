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
import base64
from pathlib import Path

# Add parent directory to path so we can import liam_client without installing
sys.path.insert(0, str(Path(__file__).parent.parent))

from liam_client import LIAMClient

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

# =============================================================================
# Workspace Onboarding (run once to get your API_KEY + private key)
# =============================================================================

def example_setup_workspace():
    """
    One-time workspace onboarding flow.

    Steps performed:
      1. Create workspace  → POST /api/auth/register        (returns apiKey)
      2. Generate ECDSA P-256 key pair locally
      3. Submit public key → POST /api/auth/submit-key
      4. Activate workspace → POST /api/auth/activate (signed with private key)

    ⚠️  Run this ONCE. Save the printed apiKey and private key — they
        are not recoverable afterwards. Put them in your .env or a
        secrets manager, then use them to initialise LIAMClient normally.
    """
    print("\n" + "=" * 50)
    print("Workspace Onboarding (run once)")
    print("=" * 50)

    # ── Configuration ─────────────────────────────────────────────────────
    NAME             = "Tech Solutions"
    INSTITUTION_ID   = "TSOL"
    INSTITUTION_NAME = "Tech Solutions"
    BASE_URL         = "https://web.askbuddy.ai/devspacexdb/api"

    # ── Step 1: Create workspace ──────────────────────────────────────────
    print("\n[1/4] Creating workspace...")
    tmp_client = LIAMClient.__new__(LIAMClient)        # bypass __init__ (no key yet)
    tmp_client.base_url = BASE_URL
    tmp_client.timeout  = 30

    import requests, json as _json
    reg_resp = requests.post(
        f"{BASE_URL}/auth/register",
        json={"name": NAME, "institutionId": INSTITUTION_ID, "institutionName": INSTITUTION_NAME},
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    reg_data = reg_resp.json()
    if reg_resp.status_code >= 400:
        print(f"  [FAIL] {reg_data.get('message')}")
        return None

    api_key = reg_data["data"]["apiKey"]
    print(f"  [OK]   apiKey: {api_key}")

    # ── Step 2: Generate ECDSA P-256 key pair ─────────────────────────────
    print("\n[2/4] Generating ECDSA P-256 key pair...")
    private_key_obj = ec.generate_private_key(ec.SECP256R1(), default_backend())

    private_key_pem = private_key_obj.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    public_key_pem_bytes = private_key_obj.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    public_key_b64 = base64.b64encode(public_key_pem_bytes).decode("utf-8")
    print("  [OK]   Key pair generated")

    # ── Step 3: Submit public key ──────────────────────────────────────────
    print("\n[3/4] Submitting public key...")
    key_resp = requests.post(
        f"{BASE_URL}/auth/submit-key",
        json={"apiKey": api_key, "publicKey": public_key_b64},
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    key_data = key_resp.json()
    if key_resp.status_code >= 400:
        print(f"  [FAIL] {key_data.get('message')}")
        return None
    print(f"  [OK]   {key_data.get('message', 'Public key accepted')}")

    # ── Step 4: Activate workspace (signed request) ────────────────────────
    print("\n[4/4] Activating workspace...")
    client = LIAMClient(api_key=api_key, private_key=private_key_pem, base_url=BASE_URL)
    act_data = client.activate_workspace(name=NAME)
    if act_data.get("status") != "Success":
        print(f"  [FAIL] {act_data.get('message')}")
        return None
    print(f"  [OK]   {act_data.get('message', 'Workspace activated')}")

    # ── Print credentials to persist ──────────────────────────────────────
    print("\n" + "=" * 50)
    print("⚠️  SAVE THESE CREDENTIALS — not recoverable after this run")
    print("=" * 50)
    print(f"\nAPI_KEY     = \"{api_key}\"")
    print(f"\nPRIVATE_KEY =\n{private_key_pem}")

    # Optionally write private key to file
    key_path = Path("private-key.pem")
    key_path.write_text(private_key_pem)
    print(f"Private key also saved to: {key_path.resolve()}")

    return api_key, private_key_pem


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

    # ── One-time setup ────────────────────────────────────────────────────
    # Set to True the very first time to register & activate your workspace.
    # After that, put the returned credentials in API_KEY / PRIVATE_KEY above
    # and set this back to False.
    RUN_ONBOARDING = False

    if RUN_ONBOARDING:
        result = example_setup_workspace()
        if not result:
            print("\n[ERROR] Onboarding failed. See output above.")
            return
        print("\nOnboarding complete. Update API_KEY and PRIVATE_KEY above, then re-run.")
        return

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