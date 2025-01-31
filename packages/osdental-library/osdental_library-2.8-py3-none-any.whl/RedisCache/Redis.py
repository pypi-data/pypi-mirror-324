import os
import json
from typing import Dict, Any, Optional
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

class RedisCacheAsync:
    def __init__(self, db: int = 1):
        self.host = os.getenv('REDIS_HOST')
        self.port = os.getenv('REDIS_PORT')
        self.password = os.getenv('REDIS_PASSWORD')
        self.db = db
        self.client = None

    async def connect(self):
        """Connect to the Redis server."""
        self.client = redis.from_url(
            f"rediss://{self.host}:{self.port}", 
            password=self.password, 
            db=self.db
        )

    async def set_dict(self, key: str, value: Dict[str, Any], ttl: Optional[int] = None):
        """Set a JSON value in the cache."""
        json_value = json.dumps(value)
        await self.client.set(key, json_value)
        if ttl:
            await self.client.expire(key, ttl)

    async def set_str(self, key: str, value: str, ttl: Optional[int] = None):
        """Set a STR value in the cache."""
        await self.client.set(key, value)
        if ttl:
            await self.client.expire(key, ttl)

    async def get_dict(self, key: str) -> Optional[Any]:
        """Get a JSON value from the cache and convert it back to a Python object."""
        json_value = await self.client.get(key)
        if json_value:
            return json.loads(json_value)
        return None

    async def get_str(self, key: str) -> Optional[Any]:
        """Get a string value from the cache."""
        return await self.client.get(key)
    
    async def delete(self, key: str) -> bool:
        """Delete a value from the cache."""
        return await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if a key exists in the cache."""
        return await self.client.exists(key)

    async def flush(self):
        """Flush all keys in the cache."""
        await self.client.flushdb()

    async def close(self):
        """Close the connection."""
        await self.client.close()
