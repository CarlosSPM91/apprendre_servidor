"""
@file test_user.py
@brief Unit and integration tests for UserRepository.
@details This file contains tests for the UserRepository, verifying correct user creation, update, deletion, and retrieval, both with mocks and real database.
"""

from unittest.mock import AsyncMock, MagicMock
import pytest
import pytest_asyncio
from sqlmodel import SQLModel, create_engine, text
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.domain.objects.user.user_dto import UserDTO
from src.infrastructure.entities.users.roles import Role
from src.infrastructure.repositories.role import RoleRepository
from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.entities.users.user import User
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO

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
def mock_session():
    """
    @brief Fixture that provides an AsyncMock session for unit tests.
    @return AsyncMock instance.
    """
    return AsyncMock()


@pytest.mark.asyncio
async def test_create_user_success(mock_session):
    """
    @brief Verifies that UserRepository.create correctly adds and returns a user using a mock session.
    @param mock_session AsyncMock session.
    """

    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    async def mock_refresh_user(user):
        user.id = 1
        
    mock_session.refresh = AsyncMock(side_effect=mock_refresh_user)

    fake_user = UserCreateDTO(
        username="testCreate",
        name="Test",
        last_name="Create",
        email="create@test.com",
        phone="123456",
        dni="12345678X",
        password="hashed_pass",
        role_id=1,
    )

    async def fake_session_gen():
        yield mock_session

    repo = UserRepository(session=fake_session_gen)

    result = await repo.create(fake_user)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

    assert isinstance(result, UserDTO)
    assert result.role == 1
    assert result.username == "testCreate"


@pytest.mark.asyncio
async def test_update_user_success(mock_session):
    """
    @brief Verifies that UserRepository.update_user correctly updates and returns a user using a mock session.
    @param mock_session AsyncMock session.
    """

    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    async def mock_refresh_user(user):
        user.id = 1
    mock_session.refresh = AsyncMock(side_effect=mock_refresh_user)

    existing_user = User(
        id=1,
        username="testCreate",
        name="Test",
        last_name="Create",
        email="create@test.com",
        phone="123456",
        dni="12345678X",
        password="hashed_pass",
        role_id=1,
    )

    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = existing_user
    mock_session.exec.return_value = mock_exec_result

    async def fake_session_gen():
        yield mock_session

    repo = UserRepository(session=fake_session_gen)

    user_update = UserUpdateDTO(user_id=1, name="Updated", username="UpdatedChar")

    result = await repo.update_user(user_update)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(existing_user)

    assert isinstance(result, UserDTO)
    assert result.name == "Updated"
    assert result.username == "UpdatedChar"


@pytest.mark.asyncio
async def test_create_user_integration(user_repository, role_repository):
    """
    @brief Verifies that UserRepository.create correctly adds and returns a user in the database.
    @param user_repository Instance of UserRepository.
    @param role_repository Instance of RoleRepository.
    """

    payload = UserCreateDTO(
        username="testCreate",
        name="Test",
        last_name="Create",
        email="create@test.com",
        phone="123456",
        dni="12345678X",
        password="hashed_pass",
        role_id=1,
    )
    await role_repository.create("Admin")
    result = await user_repository.create(payload)

    assert result.username == "testCreate"
    assert result.name == "Test"
    assert result.role == 1


@pytest.mark.asyncio
async def test_get_user_by_id_integration(user_repository, role_repository):
    """
    @brief Verifies that UserRepository.get_user_by_id retrieves the correct user by ID.
    @param user_repository Instance of UserRepository.
    @param role_repository Instance of RoleRepository.
    """

    payload = UserCreateDTO(
        username="testCreate",
        name="Test",
        last_name="Create",
        email="create@test.com",
        phone="123456",
        dni="12345678X",
        password="hashed_pass",
        role_id=1,
    )
    role = await role_repository.create("Admin")
    result = await user_repository.create(payload)
    user = await user_repository.get_user_by_id(1)

    assert user.username == "testCreate"
    assert user.name == "Test"
    assert user.role == 1


@pytest.mark.asyncio
async def test_get_user_by_username_integration(user_repository, role_repository):
    """
    @brief Verifies that UserRepository.get_user_by_username retrieves the correct user by username.
    @param user_repository Instance of UserRepository.
    @param role_repository Instance of RoleRepository.
    """

    payload = UserCreateDTO(
        username="testCreate",
        name="Test",
        last_name="Create",
        email="create@test.com",
        phone="123456",
        dni="12345678X",
        password="hashed_pass",
        role_id=1,
    )

    await role_repository.create("Admin")
    await user_repository.create(payload)
    user = await user_repository.get_user_by_username("testCreate")

    assert user.username == "testCreate"
    assert user.name == "Test"


@pytest.mark.asyncio
async def test_get_all_integration(user_repository, role_repository):
    """
    @brief Verifies that UserRepository.get_all retrieves all users from the database.
    @param user_repository Instance of UserRepository.
    @param role_repository Instance of RoleRepository.
    """

    payload = UserCreateDTO(
        username="testCreate",
        name="Test",
        last_name="Create",
        email="create@test.com",
        phone="123456",
        dni="12345678X",
        password="hashed_pass",
        role_id=1,
    )
    payload2 = UserCreateDTO(
        username="maria",
        name="Maria",
        last_name="Rojas",
        email="maria@test.com",
        phone="999999",
        dni="00011122Z",
        password="pass",
        role_id=1,
    )
    payload3 = UserCreateDTO(
        username="delete_me",
        name="Delete",
        last_name="Me",
        email="delete@test.com",
        phone="100000",
        dni="11111111D",
        password="pass",
        role_id=1,
    )

    await role_repository.create("Admin")
    await user_repository.create(payload)
    await user_repository.create(payload2)
    await user_repository.create(payload3)
    users = await user_repository.get_all()

    assert len(users) == 3
    assert users[0].username == "testCreate"
    assert users[1].username == "maria"
    assert users[2].username == "delete_me"


@pytest.mark.asyncio
async def test_update_user_integration(user_repository, role_repository):
    """
    @brief Verifies that UserRepository.update_user updates and returns the correct user.
    @param user_repository Instance of UserRepository.
    @param role_repository Instance of RoleRepository.
    """

    payload = UserCreateDTO(
        username="maria",
        name="Maria",
        last_name="Rojas",
        email="maria@test.com",
        phone="999999",
        dni="00011122Z",
        password="pass",
        role_id=1,
    )
    await role_repository.create("Admin")
    created = await user_repository.create(payload)

    update_data = UserUpdateDTO(
        user_id=created.user_id,
        name="María Updated",
        last_name="Rojas",
        username="maria",
        dni="00011122Z",
        email="maria@test.com",
        phone="999999",
        role_id=1,
        password="pass",
    )

    updated = await user_repository.update_user(update_data)

    assert updated.name == "María Updated"
    assert updated.user_id == created.user_id


@pytest.mark.asyncio
async def test_delete_user_integration(user_repository, role_repository):
    """
    @brief Verifies that UserRepository.delete removes the user and returns True.
    @param user_repository Instance of UserRepository.
    @param role_repository Instance of RoleRepository.
    """

    payload = UserCreateDTO(
        username="delete_me",
        name="Delete",
        last_name="Me",
        email="delete@test.com",
        phone="100000",
        dni="11111111D",
        password="pass",
        role_id=1,
    )
    await role_repository.create("Admin")
    created = await user_repository.create(payload)

    deleted = await user_repository.delete(created.user_id)

    assert deleted is True
