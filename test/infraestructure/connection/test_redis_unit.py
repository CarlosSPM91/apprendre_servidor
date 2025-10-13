import pytest
from unittest.mock import AsyncMock, patch
import redis.asyncio as redis_module

from src.infrastructure.connection import redis as redis_utils
from src.settings import settings


def test_get_redis_client_returns_client():
    client = redis_utils.get_redis_client()
    assert isinstance(client, redis_module.Redis)
    assert client.connection_pool.connection_kwargs["decode_responses"] is True
    assert client.connection_pool.connection_kwargs["encoding"] == "utf-8"
    assert client.connection_pool.connection_kwargs["socket_connect_timeout"] == 5
    assert client.connection_pool.connection_kwargs["socket_timeout"] == 5


@pytest.mark.asyncio
async def test_get_redis_session_yields_client_and_closes():
    mock_client = AsyncMock()
    with patch("src.infrastructure.connection.redis.get_redis_client", return_value=mock_client):
        gen = redis_utils.get_redis_session()
        client_yielded = await gen.__anext__()
        assert client_yielded == mock_client

        with pytest.raises(StopAsyncIteration):
            await gen.__anext__()
        mock_client.aclose.assert_awaited_once()
