# File: app/core/redis_conn.py

import redis.asyncio as redis
from .config import settings

class RedisClient:
    """
    A manager for the Redis connection pool and Pub/Sub operations.
    """
    def __init__(self, host, port):
        self.redis_url = f"redis://{host}:{port}"
        self.connection = None

    async def connect(self):
        """Establishes the Redis connection pool."""
        print(f"Connecting to Redis at {self.redis_url}...")
        try:
            self.connection = await redis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
            await self.connection.ping()
            print("Successfully connected to Redis.")
        except Exception as e:
            print(f"Failed to connect to Redis: {e}")
            self.connection = None

    async def disconnect(self):
        """Closes the Redis connection."""
        if self.connection:
            await self.connection.close()
            print("Disconnected from Redis.")

    async def publish(self, channel: str, message: str):
        """Publishes a message to a specific Redis channel."""
        if self.connection:
            await self.connection.publish(channel, message)

    async def subscribe(self, channel: str):
        """Subscribes to a Redis channel and returns a PubSub object."""
        if self.connection:
            pubsub = self.connection.pubsub()
            await pubsub.subscribe(channel)
            return pubsub
        return None

redis_client = RedisClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT)