"""
LIAM Client Tests

Run with: pytest tests/
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from liam_client import LIAMClient
from liam_client.client import LIAMClientError, LIAMAuthenticationError, LIAMAPIError


# =============================================================================
# Test Private Key (for testing only)
# =============================================================================

TEST_PRIVATE_KEY = """-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIBDsLbHcgMZLEPMzxJRuEqpnfHLfpHQwsC7cT7LfVYagoAcGBSuBBAAK
oUQDQgAEp2MzBqS9d3NjVg9w4Gf6R4c7OJNYwIvh7J7f7nFbJBj1WZ5C8JZK5w7y
8R8pQ7Y8j6Z5t7Y6H2Z3Z3Y3ZA==
-----END EC PRIVATE KEY-----"""


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def mock_private_key():
    """Mock the private key loading."""
    with patch('liam_client.client.serialization.load_pem_private_key') as mock:
        mock_key = MagicMock()
        mock_key.sign.return_value = b'mock_signature_bytes'
        mock.return_value = mock_key
        yield mock_key


@pytest.fixture
def client(mock_private_key):
    """Create a test client with mocked key."""
    return LIAMClient(api_key="test-api-key", private_key=TEST_PRIVATE_KEY)


# =============================================================================
# Client Initialization Tests
# =============================================================================

def test_client_initialization(mock_private_key):
    """Test client initialization."""
    client = LIAMClient(api_key="test-key", private_key=TEST_PRIVATE_KEY)
    
    assert client.api_key == "test-key"
    assert client.base_url == LIAMClient.DEFAULT_BASE_URL


def test_client_custom_base_url(mock_private_key):
    """Test client with custom base URL."""
    client = LIAMClient(
        api_key="test-key",
        private_key=TEST_PRIVATE_KEY,
        base_url="https://custom.api.com"
    )
    
    assert client.base_url == "https://custom.api.com"


def test_client_custom_timeout(mock_private_key):
    """Test client with custom timeout."""
    client = LIAMClient(api_key="test-key", private_key=TEST_PRIVATE_KEY, timeout=60)
    
    assert client.timeout == 60


def test_client_invalid_key():
    """Test client with invalid private key."""
    with pytest.raises(LIAMAuthenticationError) as exc_info:
        LIAMClient(api_key="test-key", private_key="invalid-key")
    
    assert "Failed to load private key" in str(exc_info.value)


# =============================================================================
# API Request Tests (Mocked)
# =============================================================================

@patch('liam_client.client.requests.post')
def test_health_check(mock_post, client):
    """Test health check endpoint."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "Success", "message": "OK"}
    mock_post.return_value = mock_response
    
    result = client.health_check()
    
    assert result["status"] == "Success"
    mock_post.assert_called_once()
    
    # Verify signature header was sent
    call_args = mock_post.call_args
    headers = call_args[1]["headers"]
    assert "signature" in headers
    assert "apiKey" in headers


@patch('liam_client.client.requests.post')
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


@patch('liam_client.client.requests.post')
def test_create_memory_without_tag(mock_post, client):
    """Test memory creation without tag."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "Success"}
    mock_post.return_value = mock_response
    
    result = client.create_memory(
        user_key="user123",
        content="Test memory"
    )
    
    call_args = mock_post.call_args
    request_body = call_args[1]["json"]
    assert "tag" not in request_body


@patch('liam_client.client.requests.post')
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


@patch('liam_client.client.requests.post')
def test_chat(mock_post, client):
    """Test chat endpoint."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "Success",
        "data": "Based on your memories, you prefer morning meetings."
    }
    mock_post.return_value = mock_response
    
    result = client.chat(
        user_key="user123",
        query="When do I prefer meetings?"
    )
    
    assert result["status"] == "Success"
    assert "morning" in result["data"]


@patch('liam_client.client.requests.post')
def test_api_error_handling(mock_post, client):
    """Test API error handling."""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "status": "Failed",
        "message": "Invalid request"
    }
    mock_post.return_value = mock_response
    
    with pytest.raises(LIAMAPIError) as exc_info:
        client.health_check()
    
    assert "Invalid request" in str(exc_info.value)
    assert exc_info.value.status_code == 400


@patch('liam_client.client.requests.post')
def test_api_error_with_response(mock_post, client):
    """Test API error includes response data."""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = {
        "status": "Failed",
        "message": "Unauthorized",
        "code": "AUTH_ERROR"
    }
    mock_post.return_value = mock_response
    
    with pytest.raises(LIAMAPIError) as exc_info:
        client.health_check()
    
    assert exc_info.value.response["code"] == "AUTH_ERROR"


# =============================================================================
# Tag Operations Tests (Mocked)
# =============================================================================

@patch('liam_client.client.requests.post')
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


@patch('liam_client.client.requests.post')
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


@patch('liam_client.client.requests.post')
def test_get_by_tag(mock_post, client):
    """Test getting memories by tag."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "Success",
        "data": [{"id": "1", "content": "Work memory"}]
    }
    mock_post.return_value = mock_response
    
    result = client.get_by_tag(
        user_key="user123",
        tag="work",
        limit=10,
        offset=0
    )
    
    assert result["status"] == "Success"
    assert len(result["data"]) == 1


# =============================================================================
# Environment Variable Tests
# =============================================================================

def test_from_env_missing_api_key(monkeypatch):
    """Test from_env with missing API key."""
    monkeypatch.delenv("LIAM_API_KEY", raising=False)
    monkeypatch.delenv("LIAM_PRIVATE_KEY_PATH", raising=False)
    monkeypatch.delenv("LIAM_PRIVATE_KEY", raising=False)
    
    with pytest.raises(LIAMClientError) as exc_info:
        LIAMClient.from_env()
    
    assert "LIAM_API_KEY" in str(exc_info.value)


def test_from_env_missing_private_key(monkeypatch):
    """Test from_env with missing private key."""
    monkeypatch.setenv("LIAM_API_KEY", "test-api-key")
    monkeypatch.delenv("LIAM_PRIVATE_KEY_PATH", raising=False)
    monkeypatch.delenv("LIAM_PRIVATE_KEY", raising=False)
    
    with pytest.raises(LIAMClientError) as exc_info:
        LIAMClient.from_env()
    
    assert "PRIVATE_KEY" in str(exc_info.value)
