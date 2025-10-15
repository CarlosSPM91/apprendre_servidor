"""
@file test_deletion_logs.py
@brief Integration tests for DeletionLog repository.
@details This file contains integration tests for the DeletionRepository, verifying correct creation and retrieval of deletion logs, including user and role setup.
"""

import pytest
import pytest_asyncio
from sqlmodel import SQLModel, create_engine, text
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.infrastructure.entities.users.deletion_logs import DeletionLog
from src.infrastructure.repositories.deletion_logs import DeletionRepository
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
def deletion_log_repo(async_session):
    """
    @brief Fixture that provides a DeletionRepository using the async session.
    @param async_session AsyncSession instance.
    @return DeletionRepository instance.
    """
    async def session_gen():
        yield async_session

    return DeletionRepository(session=session_gen)


@pytest.mark.asyncio
async def test_create_role(deletion_log_repo, user_repository, role_repository):
    """
    @brief Verifies that DeletionRepository can create and retrieve a deletion log entry.
    @param deletion_log_repo Instance of DeletionRepository.
    @param user_repository Instance of UserRepository.
    @param role_repository Instance of RoleRepository.
    """
    await role_repository.create("Admin")
    deleted = UserCreateDTO(
        username="deleted",
        name="deleted",
        last_name="ex",
        email="create@test.com",
        phone="123456",
        dni="12345678X",
        password="hashed_pass",
        role_id=1,
    )
    deleter = UserCreateDTO(
        username="deleter",
        name="deleter",
        last_name="ex2",
        email="create@test.com",
        phone="123456",
        dni="12345678X",
        password="hashed_pass",
        role_id=1,
    )
    await user_repository.create(deleted)
    await user_repository.create(deleter)

    deletion = DeletionLog(
        name="deleted",
        last_name="ex",
        user_id=1,
        user_who_deleted=2,
        name_who_deleted="deleter",
        last_name_who_deleted="ex2",
    )
    await deletion_log_repo.create(delete=deletion)
    result = await deletion_log_repo.find(1)

    assert result.user_id == 1
    assert result.user_who_deleted == 2
    assert result.name == "deleted"
    assert result.name_who_deleted == "deleter"
