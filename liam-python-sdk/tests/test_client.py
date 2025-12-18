"""
XDB Client Tests

Run with: pytest tests/
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock

from xdb_client import XDBClient, generate_key_pair
from xdb_client.client import XDBClientError, XDBAuthenticationError, XDBAPIError


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def key_pair():
    """Generate a test key pair."""
    return generate_key_pair()


@pytest.fixture
def client(key_pair):
    """Create a test client."""
    private_key, _ = key_pair
    return XDBClient(
        api_key="test-api-key",
        private_key_pem=private_key
    )


# =============================================================================
# Key Generation Tests
# =============================================================================

def test_generate_key_pair():
    """Test key pair generation."""
    private_pem, public_pem = generate_key_pair()
    
    assert private_pem.startswith("-----BEGIN PRIVATE KEY-----")
    assert private_pem.endswith("-----END PRIVATE KEY-----\n")
    assert public_pem.startswith("-----BEGIN PUBLIC KEY-----")
    assert public_pem.endswith("-----END PUBLIC KEY-----\n")


def test_key_pair_is_unique():
    """Test that each key pair is unique."""
    pair1 = generate_key_pair()
    pair2 = generate_key_pair()
    
    assert pair1[0] != pair2[0]  # Private keys differ
    assert pair1[1] != pair2[1]  # Public keys differ


# =============================================================================
# Client Initialization Tests
# =============================================================================

def test_client_initialization(key_pair):
    """Test client initialization."""
    private_key, _ = key_pair
    
    client = XDBClient(
        api_key="test-key",
        private_key_pem=private_key
    )
    
    assert client.api_key == "test-key"
    assert client.base_url == XDBClient.DEFAULT_BASE_URL


def test_client_custom_base_url(key_pair):
    """Test client with custom base URL."""
    private_key, _ = key_pair
    
    client = XDBClient(
        api_key="test-key",
        private_key_pem=private_key,
        base_url="https://custom.api.com"
    )
    
    assert client.base_url == "https://custom.api.com"


def test_client_invalid_private_key():
    """Test client with invalid private key."""
    with pytest.raises(XDBAuthenticationError):
        XDBClient(
            api_key="test-key",
            private_key_pem="invalid-key"
        )


# =============================================================================
# Signature Tests
# =============================================================================

def test_sign_payload(client):
    """Test payload signing."""
    payload = {"test": "data", "number": 123}
    
    signature = client._sign_payload(payload)
    
    assert isinstance(signature, str)
    assert len(signature) > 0
    # Base64 encoded signature should be ASCII
    assert signature.isascii()


def test_sign_payload_consistency(client):
    """Test that same payload produces same signature."""
    payload = {"key": "value"}
    
    sig1 = client._sign_payload(payload)
    sig2 = client._sign_payload(payload)
    
    assert sig1 == sig2


def test_sign_payload_different_for_different_data(client):
    """Test that different payloads produce different signatures."""
    payload1 = {"key": "value1"}
    payload2 = {"key": "value2"}
    
    sig1 = client._sign_payload(payload1)
    sig2 = client._sign_payload(payload2)
    
    assert sig1 != sig2


# =============================================================================
# API Request Tests (Mocked)
# =============================================================================

@patch('xdb_client.client.requests.post')
def test_health_check(mock_post, client):
    """Test health check endpoint."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "Success", "message": "OK"}
    mock_post.return_value = mock_response
    
    result = client.health_check()
    
    assert result["status"] == "Success"
    mock_post.assert_called_once()


@patch('xdb_client.client.requests.post')
def test_create_memory(mock_post, client):
    """Test memory creation."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "Success",
        "processId": "abc123"
    }
    mock_post.return_value = mock_response
    
    result = client.create_memory(
        user_key="user123",
        content="Test memory",
        tag="test"
    )
    
    assert result["status"] == "Success"
    assert result["processId"] == "abc123"
    
    # Verify request was made with correct data
    call_args = mock_post.call_args
    request_body = call_args[1]["json"]
    assert request_body["userKey"] == "user123"
    assert request_body["content"] == "Test memory"
    assert request_body["tag"] == "test"


@patch('xdb_client.client.requests.post')
def test_list_memories(mock_post, client):
    """Test listing memories."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "Success",
        "data": [{"id": "1", "content": "Memory 1"}]
    }
    mock_post.return_value = mock_response
    
    result = client.list_memories(user_key="user123", limit=10)
    
    assert result["status"] == "Success"
    assert len(result["data"]) == 1


@patch('xdb_client.client.requests.post')
def test_api_error_handling(mock_post, client):
    """Test API error handling."""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "status": "Failed",
        "message": "Invalid request"
    }
    mock_post.return_value = mock_response
    
    with pytest.raises(XDBAPIError) as exc_info:
        client.health_check()
    
    assert "Invalid request" in str(exc_info.value)
    assert exc_info.value.status_code == 400


# =============================================================================
# Tag Operations Tests (Mocked)
# =============================================================================

@patch('xdb_client.client.requests.post')
def test_list_tags(mock_post, client):
    """Test listing tags."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "Success",
        "data": ["work", "personal", "health"]
    }
    mock_post.return_value = mock_response
    
    result = client.list_tags(user_key="user123")
    
    assert result["status"] == "Success"
    assert "work" in result["data"]


@patch('xdb_client.client.requests.post')
def test_change_tag(mock_post, client):
    """Test changing tag."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "Success"}
    mock_post.return_value = mock_response
    
    result = client.change_tag(
        user_key="user123",
        old_tag="work",
        new_tag="business"
    )
    
    assert result["status"] == "Success"
    
    # Verify request body
    call_args = mock_post.call_args
    request_body = call_args[1]["json"]
    assert request_body["oldTag"] == "work"
    assert request_body["newTag"] == "business"


# =============================================================================
# Environment Variable Tests
# =============================================================================

def test_from_env_missing_api_key(key_pair, monkeypatch):
    """Test from_env with missing API key."""
    monkeypatch.delenv("XDB_API_KEY", raising=False)
    
    with pytest.raises(XDBClientError) as exc_info:
        XDBClient.from_env()
    
    assert "XDB_API_KEY" in str(exc_info.value)


def test_from_env_missing_private_key(monkeypatch):
    """Test from_env with missing private key."""
    monkeypatch.setenv("XDB_API_KEY", "test-key")
    monkeypatch.delenv("XDB_PRIVATE_KEY_PATH", raising=False)
    monkeypatch.delenv("XDB_PRIVATE_KEY", raising=False)
    
    with pytest.raises(XDBClientError) as exc_info:
        XDBClient.from_env()
    
    assert "XDB_PRIVATE_KEY" in str(exc_info.value)
