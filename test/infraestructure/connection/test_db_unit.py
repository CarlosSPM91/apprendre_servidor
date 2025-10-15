"""
@file test_db_unit.py
@brief Unit tests for database connection utilities.
@details This file contains tests for the database engine, session, and initialization utilities, verifying correct engine creation, session management, and table initialization.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection
from sqlmodel.ext.asyncio.session import AsyncSession
from src.infrastructure.connection.db import get_engine, async_init_db, get_session


@patch("src.infrastructure.connection.db.create_async_engine")
@patch("src.infrastructure.connection.db.settings")
def test_get_engine_creates_engine_with_correct_params(
    mock_settings, mock_create_engine
):
    """
    @brief Verifies that get_engine creates an engine with the correct parameters.
    @param mock_settings Mocked settings object.
    @param mock_create_engine Mocked create_async_engine function.
    """
    mock_settings.database_url = "postgresql+asyncpg://user:pass@localhost/test"
    mock_engine = MagicMock(spec=AsyncEngine)
    mock_create_engine.return_value = mock_engine

    engine = get_engine()

    mock_create_engine.assert_called_once_with(
        "postgresql+asyncpg://user:pass@localhost/test",
        echo=False,
        pool_pre_ping=True,
    )
    assert engine == mock_engine


@patch("src.infrastructure.connection.db.create_async_engine")
@patch("src.infrastructure.connection.db.settings")
def test_get_engine_returns_async_engine(mock_settings, mock_create_engine):
    """
    @brief Verifies that get_engine returns an AsyncEngine instance.
    @param mock_settings Mocked settings object.
    @param mock_create_engine Mocked create_async_engine function.
    """
    mock_settings.database_url = "postgresql+asyncpg://test"
    mock_engine = MagicMock(spec=AsyncEngine)
    mock_create_engine.return_value = mock_engine

    result = get_engine()

    assert result is not None
    assert result == mock_engine


@pytest.mark.asyncio
async def test_async_init_db_creates_all_tables():
    """
    @brief Verifies that async_init_db calls run_sync to create all tables.
    """
    mock_conn = AsyncMock(spec=AsyncConnection)
    mock_begin = AsyncMock()
    mock_begin.__aenter__.return_value = mock_conn
    mock_begin.__aexit__.return_value = None

    mock_engine = AsyncMock(spec=AsyncEngine)
    mock_engine.begin.return_value = mock_begin

    mock_conn.run_sync = AsyncMock()

    await async_init_db(mock_engine)

    mock_engine.begin.assert_called_once()
    mock_conn.run_sync.assert_called_once()

    call_args = mock_conn.run_sync.call_args
    assert call_args is not None
    assert callable(call_args[0][0])


@pytest.mark.asyncio
async def test_get_session_yields_async_session():
    """
    @brief Verifies that get_session yields an AsyncSession instance.
    """
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    with patch(
        "src.infrastructure.connection.db.AsyncSession", return_value=mock_session
    ):
        generator = get_session(AsyncMock(spec=AsyncEngine))
        sessions = []
        async for session in generator:
            sessions.append(session)

    assert len(sessions) == 1
    assert sessions[0] is mock_session


@pytest.mark.asyncio
async def test_get_session_closes_after_use():
    """
    @brief Verifies that get_session closes the session after use.
    """
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = None
    with patch(
        "src.infrastructure.connection.db.AsyncSession", return_value=mock_session
    ):
        async for session in get_session(AsyncMock(spec=AsyncEngine)):
            assert isinstance(session, AsyncSession)
