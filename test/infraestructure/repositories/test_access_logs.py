"""
@file test_access_logs.py
@brief Integration tests for AccessLog repository.
@details This file contains integration tests for the AccessRepository, verifying correct creation and retrieval of access logs, including user and role setup.
"""

import pytest
import pytest_asyncio
from sqlmodel import SQLModel, text
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.infrastructure.entities.users.accces_logs import AccessLog
from src.infrastructure.repositories.acces_logs import AccessRepository
from src.infrastructure.repositories.role import RoleRepository
from src.infrastructure.repositories.user import UserRepository

DATABASE_URL = "postgresql+psycopg://root:Adm1n@0.0.0.0:5432/apprendre_test"


@pytest_asyncio.fixture(scope="function")
async def async_engine():
    """
    @brief Fixture that creates a PostgreSQL async engine and initializes all tables.
    @return AsyncEngine instance.
    """
    engine = create_async_engine(DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session(async_engine):
    """
    @brief Fixture that provides an AsyncSession for database operations.
    @param async_engine AsyncEngine instance.
    @return AsyncSession instance.
    """
    async_session_maker = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_maker() as session:
        yield session
    await session.rollback()

@pytest.fixture
def user_repository(async_session):
    """
    @brief Fixture that provides a UserRepository using the async session.
    @param async_session AsyncSession instance.
    @return UserRepository instance.
    """
    async def session_gen():
        yield async_session
    return UserRepository(session=session_gen)

@pytest.fixture
def role_repository(async_session):
    """
    @brief Fixture that provides a RoleRepository using the async session.
    @param async_session AsyncSession instance.
    @return RoleRepository instance.
    """
    async def session_gen():
        yield async_session
    return RoleRepository(session=session_gen)

@pytest.fixture
def access_repository(async_session):
    """
    @brief Fixture that provides an AccessRepository using the async session.
    @param async_session AsyncSession instance.
    @return AccessRepository instance.
    """
    async def session_gen():
        yield async_session
    return AccessRepository(session=session_gen)


@pytest.mark.asyncio
async def test_create_and_find_access_log(access_repository, role_repository, user_repository):
    """
    @brief Verifies that AccessRepository can create and retrieve an access log entry.
    @param access_repository Instance of AccessRepository.
    @param role_repository Instance of RoleRepository.
    @param user_repository Instance of UserRepository.
    """
    await role_repository.create("Admin")
    access_user = UserCreateDTO(
        username="access",
        name="access",
        last_name="ex",
        email="access@test.com",
        phone="123456",
        dni="12345678X",
        password="hashed_pass",
        role_id=1,
    )
    await user_repository.create(access_user)

    access_log = AccessLog(
        user_id=1,
        username=access_user.username,
        acces_date=datetime.now(timezone.utc)
    )
    await access_repository.create(access_log)

    result = await access_repository.find(access_log.id)

    assert result is not None
    assert result.user_id == 1
    assert result.username == "access"
    assert result.acces_date == access_log.acces_date