"""
LIAM API Client - Synchronous Version

This module provides the main LIAMClient class for interacting with
the LIAM Memory Management API.
"""

import os
import json
import base64
import requests
from typing import Optional, Dict, Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend


class LIAMClientError(Exception):
    """Base exception for LIAM client errors."""
    pass


class LIAMAuthenticationError(LIAMClientError):
    """Raised when authentication fails."""
    pass


class LIAMAPIError(LIAMClientError):
    """Raised when the API returns an error."""
    
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class LIAMClient:
    """
    Synchronous client for the LIAM Memory Management API.
    
    Args:
        api_key: Your API key from connector registration
        private_key_pem: Your PEM-formatted ECDSA private key
        base_url: Optional custom API base URL
        timeout: Request timeout in seconds (default: 30)
    
    Example:
        >>> client = LIAMClient(
        ...     api_key="your-api-key",
        ...     private_key_pem=open('private_key.pem').read()
        ... )
        >>> client.health_check()
        {'status': 'Success', 'message': 'OK'}
    """
    
    DEFAULT_BASE_URL = "https://api.liam.netxd.com/api"
    
    def __init__(
        self,
        api_key: str,
        private_key_pem: str,
        base_url: str = None,
        timeout: int = 30
    ):
        self.api_key = api_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout
        
        # Load private key
        try:
            key_bytes = private_key_pem.encode() if isinstance(private_key_pem, str) else private_key_pem
            self.private_key = serialization.load_pem_private_key(
                key_bytes,
                password=None,
                backend=default_backend()
            )
        except Exception as e:
            raise LIAMAuthenticationError(f"Failed to load private key: {e}")
    
    @classmethod
    def from_env(cls, base_url: str = None) -> "LIAMClient":
        """
        Create client from environment variables.
        
        Environment variables:
            LIAM_API_KEY: Your API key
            LIAM_PRIVATE_KEY_PATH: Path to private key file
            LIAM_PRIVATE_KEY: Private key content (alternative to path)
            LIAM_BASE_URL: Optional custom base URL
        
        Returns:
            LIAMClient instance
        """
        api_key = os.environ.get("LIAM_API_KEY")
        if not api_key:
            raise LIAMClientError("LIAM_API_KEY environment variable not set")
        
        # Try path first, then direct key
        key_path = os.environ.get("LIAM_PRIVATE_KEY_PATH")
        if key_path:
            with open(key_path, 'r') as f:
                private_key = f.read()
        else:
            private_key = os.environ.get("LIAM_PRIVATE_KEY")
            if not private_key:
                raise LIAMClientError(
                    "Either LIAM_PRIVATE_KEY_PATH or LIAM_PRIVATE_KEY must be set"
                )
        
        base_url = base_url or os.environ.get("LIAM_BASE_URL")
        
        return cls(api_key=api_key, private_key_pem=private_key, base_url=base_url)
    
    def _sign_payload(self, payload: Dict[str, Any]) -> str:
        """
        Sign a payload using ECDSA with SHA-256.
        
        Args:
            payload: The request body as a dictionary
            
        Returns:
            Base64-encoded DER signature
        """
        # Convert to compact JSON (no extra spaces)
        payload_str = json.dumps(payload, separators=(',', ':'))
        payload_bytes = payload_str.encode('utf-8')
        
        # Sign with ECDSA SHA-256 (returns DER format)
        signature = self.private_key.sign(
            payload_bytes,
            ec.ECDSA(hashes.SHA256())
        )
        
        return base64.b64encode(signature).decode('utf-8')
    
    def _make_request(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        timeout: int = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to the API.
        
        Args:
            endpoint: API endpoint (e.g., 'memory/create')
            payload: Request body
            timeout: Optional request timeout override
            
        Returns:
            API response as dictionary
            
        Raises:
            LIAMAPIError: On API errors
            requests.exceptions.RequestException: On network errors
        """
        url = f"{self.base_url}/{endpoint}"
        signature = self._sign_payload(payload)
        
        headers = {
            "Content-Type": "application/json",
            "apiKey": self.api_key,
            "signature": signature
        }
        
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=timeout or self.timeout
        )
        
        # Parse response
        try:
            data = response.json()
        except json.JSONDecodeError:
            raise LIAMAPIError(
                f"Invalid JSON response: {response.text}",
                status_code=response.status_code
            )
        
        # Check for errors
        if response.status_code >= 400:
            raise LIAMAPIError(
                data.get('message', 'Unknown error'),
                status_code=response.status_code,
                response=data
            )
        
        return data
    
    # ==================== Memory Operations ====================
    
    def create_memory(
        self,
        user_key: str,
        content: str,
        tag: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new memory entry.
        
        Args:
            user_key: The user's unique key
            content: The memory content to store
            tag: Optional tag for categorization
            session_id: Optional session identifier
            
        Returns:
            API response with status and process ID
        """
        payload = {"userKey": user_key, "content": content}
        if tag:
            payload["tag"] = tag
        if session_id:
            payload["sessionId"] = session_id
        return self._make_request("memory/create", payload)
    
    def create_memory_with_image(
        self,
        user_key: str,
        content: str,
        image_base64: str,
        tag: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new memory with an associated image.
        
        Args:
            user_key: The user's unique key
            content: The memory content to store
            image_base64: Base64-encoded image data
            tag: Optional tag for categorization
            session_id: Optional session identifier
            
        Returns:
            API response with status and process ID
        """
        payload = {"userKey": user_key, "content": content, "image": image_base64}
        if tag:
            payload["tag"] = tag
        if session_id:
            payload["sessionId"] = session_id
        return self._make_request("memory/create-with-image", payload)
    
    def memory_status(
        self,
        user_key: str,
        process_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check the status of a memory processing operation.
        
        Args:
            user_key: The user's unique key
            process_id: The process ID to check status for
            
        Returns:
            API response with processing status
        """
        payload = {"userKey": user_key}
        if process_id:
            payload["processId"] = process_id
        return self._make_request("memory/status", payload)
    
    def list_memories(
        self,
        user_key: str,
        query: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Retrieve a list of memories for a user.
        
        Args:
            user_key: The user's unique key
            query: Optional search query to filter memories
            limit: Maximum number of results (default: 50)
            
        Returns:
            API response with list of memories
        """
        payload = {"userKey": user_key, "limit": limit}
        if query:
            payload["query"] = query
        return self._make_request("memory/list", payload)
    
    def chat(
        self,
        user_key: str,
        query: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Chat with memory context.
        
        Args:
            user_key: The user's unique key
            query: The chat query/question
            session_id: Optional session identifier for context
            
        Returns:
            API response with chat result
        """
        payload = {"userKey": user_key, "query": query}
        if session_id:
            payload["sessionId"] = session_id
        return self._make_request("memory/chat", payload)
    
    def summarize_memory(
        self,
        user_key: str,
        memory_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Summarize memories for a user.
        
        Args:
            user_key: The user's unique key
            memory_id: Optional specific memory ID to summarize
            
        Returns:
            API response with summary
        """
        payload = {"userKey": user_key}
        if memory_id:
            payload["memoryId"] = memory_id
        return self._make_request("memory/summarize", payload)
    
    def forget_memory(
        self,
        user_key: str,
        memory_id: str,
        permanent: bool = False
    ) -> Dict[str, Any]:
        """
        Delete or forget a memory.
        
        Args:
            user_key: The user's unique key
            memory_id: The ID of the memory to forget
            permanent: Whether to permanently delete (default: False)
            
        Returns:
            API response with status
        """
        payload = {
            "userKey": user_key,
            "memoryId": memory_id,
            "permanent": permanent
        }
        return self._make_request("memory/forget", payload)
    
    # ==================== Tag Operations ====================
    
    def list_tags(self, user_key: str) -> Dict[str, Any]:
        """
        List all tags for a user.
        
        Args:
            user_key: The user's unique key
            
        Returns:
            API response with list of tags
        """
        return self._make_request("memory/list-tags", {"userKey": user_key})
    
    def add_tag(
        self,
        user_key: str,
        memory_id: str,
        tag: str
    ) -> Dict[str, Any]:
        """
        Add a tag to a memory.
        
        Args:
            user_key: The user's unique key
            memory_id: The ID of the memory
            tag: The tag to add
            
        Returns:
            API response with status
        """
        payload = {"userKey": user_key, "memoryId": memory_id, "tag": tag}
        return self._make_request("memory/add-tag", payload)
    
    def get_by_tag(
        self,
        user_key: str,
        tag: str,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get memories by tag.
        
        Args:
            user_key: The user's unique key
            tag: The tag to filter by
            limit: Maximum number of results (default: 50)
            offset: Number of results to skip for pagination
            
        Returns:
            API response with list of memories
        """
        payload = {
            "userKey": user_key,
            "tag": tag,
            "limit": limit,
            "offset": offset
        }
        return self._make_request("memory/get-by-tag", payload)
    
    def change_tag(
        self,
        user_key: str,
        old_tag: str,
        new_tag: str
    ) -> Dict[str, Any]:
        """
        Change tag for memories.
        
        Args:
            user_key: The user's unique key
            old_tag: The current tag name
            new_tag: The new tag name
            
        Returns:
            API response with status
        """
        payload = {"userKey": user_key, "oldTag": old_tag, "newTag": new_tag}
        return self._make_request("memory/change-tag", payload)
    
    # ==================== Health Check ====================
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check API health status.
        
        Returns:
            API response with health status
        """
        return self._make_request("memory/health", {"ping": "test"})
