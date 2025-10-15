"""
@file test_redis_unit.py
@brief Unit tests for Redis connection utilities.
@details This file contains tests for the Redis connection utility functions, verifying correct client configuration and session management.
"""

import pytest
from unittest.mock import AsyncMock, patch
import redis.asyncio as redis_module

from src.infrastructure.connection import redis as redis_utils
from src.settings import settings


def test_get_redis_client_returns_client():
    """
    @brief Verifies that get_redis_client returns a Redis client with correct configuration.
    """
    client = redis_utils.get_redis_client()
    assert isinstance(client, redis_module.Redis)
    assert client.connection_pool.connection_kwargs["decode_responses"] is True
    assert client.connection_pool.connection_kwargs["encoding"] == "utf-8"
    assert client.connection_pool.connection_kwargs["socket_connect_timeout"] == 5
    assert client.connection_pool.connection_kwargs["socket_timeout"] == 5


@pytest.mark.asyncio
async def test_get_redis_session_yields_client_and_closes():
    """
    @brief Verifies that get_redis_session yields a client and closes it after use.
    """
    mock_client = AsyncMock()
    with patch("src.infrastructure.connection.redis.get_redis_client", return_value=mock_client):
        gen = redis_utils.get_redis_session()
        client_yielded = await gen.__anext__()
        assert client_yielded == mock_client

        with pytest.raises(StopAsyncIteration):
            await gen.__anext__()
        mock_client.aclose.assert_awaited_once()
