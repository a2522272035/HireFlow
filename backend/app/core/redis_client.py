from __future__ import annotations

import json
from typing import Any

import redis.asyncio as redis

from app.config import settings


class RedisClient:
    """Redis client wrapper for async operations."""

    def __init__(self) -> None:
        self._client: redis.Redis | None = None

    async def connect(self) -> None:
        """Initialize Redis connection."""
        self._client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )

    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._client = None

    async def get(self, key: str) -> str | None:
        """Get value by key."""
        if not self._client:
            await self.connect()
        return await self._client.get(key)

    async def set(
        self,
        key: str,
        value: str,
        expire: int | None = None,
    ) -> bool:
        """Set value with optional expiration (seconds)."""
        if not self._client:
            await self.connect()
        return await self._client.set(key, value, ex=expire)

    async def delete(self, key: str) -> int:
        """Delete key."""
        if not self._client:
            await self.connect()
        return await self._client.delete(key)

    async def get_json(self, key: str) -> Any | None:
        """Get and parse JSON value."""
        value = await self.get(key)
        if value:
            return json.loads(value)
        return None

    async def set_json(
        self,
        key: str,
        value: Any,
        expire: int | None = None,
    ) -> bool:
        """Set JSON value."""
        return await self.set(key, json.dumps(value), expire)


# Global Redis client instance
redis_client = RedisClient()
