import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection
from sqlmodel import SQLModel, text
from sqlmodel.ext.asyncio.session import AsyncSession
from src.infrastructure.connection.db import get_engine, async_init_db, get_session


@pytest_asyncio.fixture
async def sqlite_engine():
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )
    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def test_db_engine(monkeypatch):
    test_db_url = "postgresql+psycopg://root:Adm1n@0.0.0.0:5432/apprendre_test"
    monkeypatch.setattr(
        "src.infrastructure.connection.db.settings.database_url", test_db_url
    )

    engine_postgre = get_engine()

    await async_init_db(engine_postgre)

    yield engine_postgre
    async with engine_postgre.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine_postgre.dispose()


@pytest.mark.asyncio
async def test_async_init_db_creates_tables_successfully(sqlite_engine):
    await async_init_db(sqlite_engine)
    async with sqlite_engine.connect() as conn:
        result = await conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table'")
        )
        tables = [row[0] for row in result]
        expected_tables = ["users", "roles", "access_log"]
        for table in expected_tables:
            assert table in tables, f"Table {table} not created"


@pytest.mark.asyncio
async def test_get_session_provides_working_session(sqlite_engine):
    await async_init_db(sqlite_engine)
    async for session in get_session(sqlite_engine):
        from sqlmodel import select
        from src.infrastructure.entities.users.user import User

        result = await session.exec(select(User))
        users = result.all()
        assert isinstance(users, list)
        assert len(users) == 0


@pytest.mark.asyncio
async def test_full_database_workflow(test_db_engine):
    from src.infrastructure.entities.users.user import User
    from src.infrastructure.entities.users.roles import Role
    from sqlmodel import select

    async for session in get_session(test_db_engine):
        role=Role(role_name="Admin")
        session.add(role)
        await session.commit()
        await session.refresh(role)
        
        user = User(
            username="testuser",
            email="test@example.com",
            dni="1234567A",
            name="Test",
            last_name="Prueba",
            password="1234",
            phone="123456789",
            role_id=1,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        user_id = user.id

    async for session in get_session(test_db_engine):
        found_user = (
            await session.exec(select(User).where(User.id == user_id))
        ).first()
        assert found_user is not None
        assert found_user.username == "testuser"
        assert found_user.email == "test@example.com"
        assert found_user.dni == "1234567A"
