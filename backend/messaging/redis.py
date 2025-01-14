import asyncio
import os
from typing import AsyncGenerator, Optional
from redis.asyncio import Redis

class AsyncRedisClient:
    """
    A utility class to manage Redis connections and 
    provide methods for publishing and subscribing to channels.

    Attributes:
        host (str): The Redis server host.
        port (int): The Redis server port.
        decode_responses (bool): Whether to decode Redis responses into strings.
        client (Optional[redis.Redis]): The Redis client instance.
    """

    def __init__(
            self,
            host: Optional[str] = None,
            port: Optional[int] = None
    ):
        """
        Initializes the RedisClient with the given host, port, and response decoding preference.

        Args:
            host (Optional[str]): The Redis server host.
            port (Optional[int]): The Redis server port.
            decode_responses (bool): Whether to decode Redis responses into strings (default: True).
        """
        self.host: str = host or os.getenv("REDIS_HOST", "localhost")
        self.port: int = port or int(os.getenv("REDIS_PORT", "6379"))
        self.redis = Redis(host=self.host, port=self.port, decode_responses=True)

    async def subscribe(self, channel: str) -> AsyncGenerator[str, None]:
        """
        Subscribe to a Redis channel and yield messages asynchronously.
        """
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)

        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message and message["type"] == "message":
                    yield message["data"]
                await asyncio.sleep(0.1)  # Allow the event loop to process other tasks
        finally:
            await pubsub.unsubscribe(channel)
            await pubsub.close()

    async def publish(self, channel: str, message: str):
        """
        Publish a message to a Redis channel.
        """
        await self.redis.publish(channel, message)

    async def close(self):
        """
        Close the Redis connection.
        """
        await self.redis.close()

    async def unsubscribe(self, pubsub, channel: str):
        """Unsubscribe from a Redis channel."""
        await pubsub.unsubscribe(channel)
        await pubsub.close()
