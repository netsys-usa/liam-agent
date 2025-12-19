"""
LIAM API Client - Asynchronous Version

This module provides the LIAMClientAsync class for high-performance
asynchronous interactions with the LIAM Memory Management API.

Requires: pip install aiohttp
"""

import json
import asyncio
from typing import Optional, Dict, Any, List

import aiohttp

from .client import LIAMClientError, LIAMAPIError


class LIAMClientAsync:
    """
    Asynchronous client for the LIAM Memory Management API.
    
    Best used as an async context manager for connection pooling:
    
        async with LIAMClientAsync(api_key="your-key") as client:
            result = await client.create_memory(...)
    
    Args:
        api_key: Your API key from connector registration
        base_url: Optional custom API base URL
        timeout: Request timeout in seconds (default: 30)
    """
    
    DEFAULT_BASE_URL = "https://api.liam.netxd.com/api"
    
    def __init__(
        self,
        api_key: str,
        base_url: str = None,
        timeout: int = 30
    ):
        self.api_key = api_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self) -> "LIAMClientAsync":
        """Async context manager entry - creates session."""
        self._session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - closes session."""
        if self._session:
            await self._session.close()
            self._session = None
    
    async def close(self):
        """Explicitly close the session."""
        if self._session:
            await self._session.close()
            self._session = None
    
    async def _make_request(
        self,
        endpoint: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make an async request to the API.
        
        Args:
            endpoint: API endpoint (e.g., 'memory/create')
            payload: Request body
            
        Returns:
            API response as dictionary
            
        Raises:
            LIAMAPIError: On API errors
            aiohttp.ClientError: On network errors
        """
        url = f"{self.base_url}/{endpoint}"
        
        headers = {
            "Content-Type": "application/json",
            "apiKey": self.api_key
        }
        
        # Use existing session or create temporary one
        if self._session:
            async with self._session.post(url, json=payload, headers=headers) as response:
                try:
                    data = await response.json()
                except json.JSONDecodeError:
                    text = await response.text()
                    raise LIAMAPIError(f"Invalid JSON response: {text}", response.status)
                
                if response.status >= 400:
                    raise LIAMAPIError(
                        data.get('message', 'Unknown error'),
                        response.status,
                        data
                    )
                return data
        else:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    try:
                        data = await response.json()
                    except json.JSONDecodeError:
                        text = await response.text()
                        raise LIAMAPIError(f"Invalid JSON response: {text}", response.status)
                    
                    if response.status >= 400:
                        raise LIAMAPIError(
                            data.get('message', 'Unknown error'),
                            response.status,
                            data
                        )
                    return data
    
    # ==================== Memory Operations ====================
    
    async def create_memory(
        self,
        user_key: str,
        content: str,
        tag: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new memory asynchronously."""
        payload = {"userKey": user_key, "content": content}
        if tag:
            payload["tag"] = tag
        if session_id:
            payload["sessionId"] = session_id
        return await self._make_request("memory/create", payload)
    
    async def create_memory_with_image(
        self,
        user_key: str,
        content: str,
        image_base64: str,
        tag: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new memory with image asynchronously."""
        payload = {"userKey": user_key, "content": content, "image": image_base64}
        if tag:
            payload["tag"] = tag
        if session_id:
            payload["sessionId"] = session_id
        return await self._make_request("memory/create-with-image", payload)
    
    async def memory_status(
        self,
        user_key: str,
        process_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Check memory processing status asynchronously."""
        payload = {"userKey": user_key}
        if process_id:
            payload["processId"] = process_id
        return await self._make_request("memory/status", payload)
    
    async def list_memories(
        self,
        user_key: str,
        query: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """List memories asynchronously."""
        payload = {"userKey": user_key, "limit": limit}
        if query:
            payload["query"] = query
        return await self._make_request("memory/list", payload)
    
    async def chat(
        self,
        user_key: str,
        query: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Chat with memory context asynchronously."""
        payload = {"userKey": user_key, "query": query}
        if session_id:
            payload["sessionId"] = session_id
        return await self._make_request("memory/chat", payload)
    
    async def summarize_memory(
        self,
        user_key: str,
        memory_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Summarize memories asynchronously."""
        payload = {"userKey": user_key}
        if memory_id:
            payload["memoryId"] = memory_id
        return await self._make_request("memory/summarize", payload)
    
    async def forget_memory(
        self,
        user_key: str,
        memory_id: str,
        permanent: bool = False
    ) -> Dict[str, Any]:
        """Forget a memory asynchronously."""
        payload = {"userKey": user_key, "memoryId": memory_id, "permanent": permanent}
        return await self._make_request("memory/forget", payload)
    
    # ==================== Tag Operations ====================
    
    async def list_tags(self, user_key: str) -> Dict[str, Any]:
        """List all tags asynchronously."""
        return await self._make_request("memory/list-tags", {"userKey": user_key})
    
    async def add_tag(
        self,
        user_key: str,
        memory_id: str,
        tag: str
    ) -> Dict[str, Any]:
        """Add a tag asynchronously."""
        payload = {"userKey": user_key, "memoryId": memory_id, "tag": tag}
        return await self._make_request("memory/add-tag", payload)
    
    async def get_by_tag(
        self,
        user_key: str,
        tag: str,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get memories by tag asynchronously."""
        payload = {"userKey": user_key, "tag": tag, "limit": limit, "offset": offset}
        return await self._make_request("memory/get-by-tag", payload)
    
    async def change_tag(
        self,
        user_key: str,
        old_tag: str,
        new_tag: str
    ) -> Dict[str, Any]:
        """Change tag asynchronously."""
        payload = {"userKey": user_key, "oldTag": old_tag, "newTag": new_tag}
        return await self._make_request("memory/change-tag", payload)
    
    # ==================== Health Check ====================
    
    async def health_check(self) -> Dict[str, Any]:
        """Check API health status asynchronously."""
        return await self._make_request("memory/health", {"ping": "test"})
    
    # ==================== Batch Operations ====================
    
    async def create_memories_batch(
        self,
        user_key: str,
        memories: List[Dict[str, str]],
        concurrency: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Create multiple memories concurrently.
        
        Args:
            user_key: The user's unique key
            memories: List of dicts with 'content' and optional 'tag' keys
            concurrency: Max concurrent requests (default: 10)
            
        Returns:
            List of API responses
            
        Example:
            memories = [
                {"content": "Memory 1", "tag": "work"},
                {"content": "Memory 2", "tag": "personal"},
            ]
            results = await client.create_memories_batch("user_key", memories)
        """
        semaphore = asyncio.Semaphore(concurrency)
        
        async def create_with_limit(memory: Dict[str, str]) -> Dict[str, Any]:
            async with semaphore:
                return await self.create_memory(
                    user_key=user_key,
                    content=memory["content"],
                    tag=memory.get("tag"),
                    session_id=memory.get("session_id")
                )
        
        tasks = [create_with_limit(m) for m in memories]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def get_all_tagged_memories(
        self,
        user_key: str,
        tags: List[str],
        concurrency: int = 10
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get memories for multiple tags concurrently.
        
        Args:
            user_key: The user's unique key
            tags: List of tags to fetch
            concurrency: Max concurrent requests (default: 10)
            
        Returns:
            Dict mapping tag names to their API responses
        """
        semaphore = asyncio.Semaphore(concurrency)
        
        async def get_with_limit(tag: str) -> Dict[str, Any]:
            async with semaphore:
                return await self.get_by_tag(user_key, tag)
        
        tasks = [get_with_limit(tag) for tag in tags]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {tag: result for tag, result in zip(tags, results)}
