
import redis.asyncio as redis
from src.settings import settings

def get_redis_client():
    return redis.from_url(
        url=settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5
    )

async def get_redis_session():
    client = get_redis_client()
    try:
        yield client
    finally:
        await client.aclose()