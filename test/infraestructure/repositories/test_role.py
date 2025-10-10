import pytest
import pytest_asyncio
from sqlmodel import SQLModel, create_engine, text
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


from src.domain.objects.role.role_dto import RoleDTO
from src.infrastructure.entities.users.roles import Role
from src.infrastructure.repositories.role import RoleRepository
from src.infrastructure.repositories.user import UserRepository
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
def role_repository(async_session):
    async def session_gen():
        yield async_session
    return RoleRepository(session=session_gen)


@pytest.mark.asyncio
async def test_create_role(role_repository):
    result = await role_repository.create("Admin")


    assert result.role_id == 1
    assert result.role_name == "Admin"


@pytest.mark.asyncio
async def test_get_role_id(role_repository):
    await role_repository.create("Admin")
    result: RoleDTO = await role_repository.find_role(role_id=1)

    assert result.role_name == "Admin"
    assert result.role_id == 1


@pytest.mark.asyncio
async def test_get_all(role_repository):
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
async def test_update_role(role_repository):
    await role_repository.create("Admin")
    role_before_upt= await role_repository.find_role(1)
    role_upt= RoleDTO(role_id=1, role_name="User")
    result = await role_repository.update_role(role_upt)
    role_after = await role_repository.find_role(1)


    assert role_before_upt.role_name != role_after.role_name
    assert role_before_upt.role_id == role_after.role_id


@pytest.mark.asyncio
async def test_delete_role(role_repository):
    role = await role_repository.create("Admin")

    deleted = await role_repository.delete(role.role_id)

    assert deleted is True
