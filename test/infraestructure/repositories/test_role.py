"""
@file test_role.py
@brief Unit and integration tests for RoleRepository.
@details This file contains tests for the RoleRepository, verifying correct role creation, update, deletion, and retrieval, both with mocks and real database.
"""

from unittest.mock import AsyncMock, MagicMock, Mock
import pytest
import pytest_asyncio
from sqlmodel import SQLModel, create_engine, text
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.role.role_dto import RoleDTO
from src.infrastructure.entities.users.roles import Role
from src.infrastructure.repositories.role import RoleRepository
from src.infrastructure.repositories.user import UserRepository
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
async def test_get_role_by_name_success(mock_session):
    """
    @brief Verifies that RoleRepository.find_role_by_name correctly retrieves a role using a mock session.
    @param mock_session AsyncMock session.
    """

    fake_role = Role(id=1, role_name="Admin")

    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value=fake_role
    mock_session.exec.return_value= mock_exec_result

    async def fake_session_gen():
        yield mock_session

    repo = RoleRepository(session=fake_session_gen)

    result = await repo.find_role_by_name("Admin")

    mock_session.exec.assert_called_once()
    assert isinstance(result, Role)
    assert result.id == 1
    assert result.role_name == "Admin"



@pytest.mark.asyncio
async def test_create_role_success(mock_session):
    """
    @brief Verifies that RoleRepository.create correctly adds and returns a role using a mock session.
    @param mock_session AsyncMock session.
    """

    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    async def mock_refresh_role(role):
        role.id = 1
    
    mock_session.refresh = AsyncMock(side_effect=mock_refresh_role)

    fake_role = Role(role_name="Admin")
    fake_role.id = 1 

    async def fake_session_gen():
        yield mock_session

    repo = RoleRepository(session=fake_session_gen)

    result = await repo.create("Admin")

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(fake_role)

    assert isinstance(result, RoleDTO)
    assert result.role_id == 1
    assert result.role_name == "Admin"

@pytest.mark.asyncio
async def test_update_role_success(mock_session):
    """
    @brief Verifies that RoleRepository.update_role correctly updates and returns a role using a mock session.
    @param mock_session AsyncMock session.
    """

    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    async def mock_refresh_role(role):
        role.id = 1

    mock_session.refresh = AsyncMock(side_effect=mock_refresh_role)

    existing_role = Role(id=1, role_name="Admin")

    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value=existing_role
    mock_session.exec.return_value= mock_exec_result

    async def fake_session_gen():
        yield mock_session

    repo = RoleRepository(session=fake_session_gen)

    role_update = RoleDTO(role_id=1, role_name="Student")

    result = await repo.update_role(role_update)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(existing_role)

    assert isinstance(result, RoleDTO)
    assert result.role_id == 1
    assert result.role_name == "Student"
    


@pytest.mark.asyncio
async def test_create_role_integration(role_repository):
    """
    @brief Verifies that RoleRepository.create correctly adds and returns a role in the database.
    @param role_repository Instance of RoleRepository.
    """
    result = await role_repository.create("Admin")


    assert result.role_id == 1
    assert result.role_name == "Admin"


@pytest.mark.asyncio
async def test_get_role_id_integration(role_repository):
    """
    @brief Verifies that RoleRepository.find_role retrieves the correct role by ID.
    @param role_repository Instance of RoleRepository.
    """
    await role_repository.create("Admin")
    result: RoleDTO = await role_repository.find_role(role_id=1)

    assert result.role_name == "Admin"
    assert result.role_id == 1


@pytest.mark.asyncio
async def test_get_all_integration(role_repository):
    """
    @brief Verifies that RoleRepository.get_roles retrieves all roles from the database.
    @param role_repository Instance of RoleRepository.
    """
    await role_repository.create("Admin")
    await role_repository.create("Parent")
    await role_repository.create("Student")
    await role_repository.create("Professor")

    roles = await role_repository.get_roles()

    assert len(roles)==4
    assert roles[0].role_name=="Admin"
    assert roles[1].role_name=="Parent"
    assert roles[2].role_name=="Student"
    assert roles[3].role_name=="Professor"

@pytest.mark.asyncio
async def test_update_role_integration(role_repository):
    """
    @brief Verifies that RoleRepository.update_role updates and returns the correct role.
    @param role_repository Instance of RoleRepository.
    """
    await role_repository.create("Admin")
    role_before_upt= await role_repository.find_role(1)
    role_upt= RoleDTO(role_id=1, role_name="User")
    result = await role_repository.update_role(role_upt)
    role_after = await role_repository.find_role(1)


    assert role_before_upt.role_name != role_after.role_name
    assert role_before_upt.role_id == role_after.role_id


@pytest.mark.asyncio
async def test_delete_role_integration(role_repository):
    """
    @brief Verifies that RoleRepository.delete removes the role and returns True.
    @param role_repository Instance of RoleRepository.
    """
    role = await role_repository.create("Admin")

    deleted = await role_repository.delete(role.role_id)

    assert deleted is True
