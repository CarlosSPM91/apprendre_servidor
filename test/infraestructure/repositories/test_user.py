import pytest
import pytest_asyncio
from sqlmodel import SQLModel, create_engine, text
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


from src.infrastructure.entities.users.roles import Role
from src.infrastructure.repositories.role import RoleRepository
from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.entities.users.user import User
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO

DATABASE_URL = "postgresql+psycopg://root:Adm1n@0.0.0.0:5432/apprendre_test"


@pytest_asyncio.fixture(scope="function")
async def async_engine():
    engine = create_async_engine(DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine

    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session(async_engine):
    async_session_maker = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_maker() as session:
        yield session

    await session.rollback()


@pytest.fixture
def user_repository(async_session):
    async def session_gen():
        yield async_session
    return UserRepository(session=session_gen)

@pytest.fixture
def role_repository(async_session):
    async def session_gen():
        yield async_session
    return RoleRepository(session=session_gen)


@pytest.mark.asyncio
async def test_create_user(user_repository, role_repository):
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
async def test_get_user_by_id(user_repository, role_repository):
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
async def test_get_user_by_username(user_repository, role_repository):
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
    user = await user_repository.get_user_by_username("testCreate")

    assert user.username == "testCreate"
    assert user.name == "Test"


@pytest.mark.asyncio
async def test_get_all(user_repository, role_repository):
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

    role = await role_repository.create("Admin")
    await user_repository.create(payload)
    await user_repository.create(payload2)
    await user_repository.create(payload3)
    users = await user_repository.get_all()

    assert len(users)==3
    assert users[0].username=="testCreate"
    assert users[1].username=="maria"
    assert users[2].username=="delete_me"

@pytest.mark.asyncio
async def test_update_user(user_repository, role_repository):
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
    role = await role_repository.create("Admin")
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
async def test_delete_user(user_repository, role_repository):
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
