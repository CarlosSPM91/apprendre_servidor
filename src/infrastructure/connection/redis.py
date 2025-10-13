"""
Redis connection utilities.

Provides helper functions to create and manage an asynchronous Redis client
and session for use with FastAPI or other async components.

:author: Carlos S. Paredes Morillo
"""

import redis.asyncio as redis
from src.settings import settings


def get_redis_client() -> redis.Redis:
    """
    Create and return a Redis client.

    Returns:
        redis.Redis: Asynchronous Redis client instance.

    Notes:
        The client is configured with UTF-8 encoding and a 5-second socket timeout.
    """
    return redis.from_url(
        url=settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5
    )


async def get_redis_session():
    """
    Generate an asynchronous Redis session for use with FastAPI dependencies.

    Yields:
        redis.Redis: An asynchronous Redis client session.

    Notes:
        Ensures the client is properly closed after use.
    """
    client = get_redis_client()
    try:
        yield client
    finally:
        await client.aclose()
