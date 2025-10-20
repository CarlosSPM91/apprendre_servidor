from unittest.mock import AsyncMock, MagicMock
import pytest

from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.infrastructure.entities.student_info.student import Student
from src.infrastructure.entities.users.user import User
from src.infrastructure.repositories.student import StudentRepository
from src.infrastructure.repositories.user import UserRepository


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    session.delete = AsyncMock()
    session.exec = AsyncMock()
    return session

@pytest.fixture
def student_repository(mock_session):
    async def session_gen():
        yield mock_session
    return StudentRepository(session=session_gen)

@pytest.fixture
def user_repository(mock_session):
    async def session_gen():
        yield mock_session
    return UserRepository(session=session_gen)

@pytest.fixture
def fake_student():
    return Student(
        id=1,
        user_id=1,
        observations="No observaciones"
    )

@pytest.fixture
def fake_user():
    return User(
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

@pytest.fixture
def fake_user_create_dto():
    return UserCreateDTO(
        username="testCreate",
        name="Test",
        last_name="Create",
        email="create@test.com",
        phone="123456",
        dni="12345678X",
        password="hashed_pass",
        role_id=1,
    )

@pytest.mark.asyncio
async def test_init():
    mock_session_test = MagicMock()
    student_repository = StudentRepository(mock_session_test)
    assert student_repository.session == mock_session_test

@pytest.mark.asyncio
async def test_get_student_succes(fake_student, student_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = fake_student
    

    mock_session.exec = AsyncMock(return_value=mock_exec_result)

    result = await student_repository.get_student(1)

    assert result == fake_student
    assert result.id == 1
    assert result.user_id == 1
    mock_session.exec.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_student_full_info_succes(fake_student, student_repository, mock_session):
    fake_user = User(
        id=1,
        username="testUser",
        name="Test",
        last_name="User",
        email="test@test.com",
        phone="123456",
        dni="12345678X",
        password="hashed_pass",
        role_id=1,
    )
    
    mock_student_result = MagicMock()
    mock_student_result.first.return_value = (fake_student, fake_user)
    

    mock_empty_result = MagicMock()
    mock_empty_result.all.return_value = []
    

    mock_session.exec = AsyncMock(side_effect=[
        mock_student_result,  
        mock_empty_result,   
        mock_empty_result,    
        mock_empty_result,    
    ])

    result = await student_repository.get_student_full_info(1)

    assert result.student_id == 1
    assert result.user_id == 1
    assert result.name == "Test"
    assert result.last_name == "User"
    assert mock_session.exec.await_count == 4

@pytest.mark.asyncio
async def test_create_student_success(fake_student, student_repository, mock_session):

    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    result = await student_repository.create(fake_student)

    assert result.user_id == 1
    assert result.observations == "No observaciones"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_create_user_and_student_success(fake_user_create_dto, fake_student, user_repository, student_repository, mock_session):

    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    
    async def mock_refresh_user(user):
        user.id = 1
    mock_session.refresh = AsyncMock(side_effect=mock_refresh_user)

    result_user = await user_repository.create(fake_user_create_dto)
    
    mock_session.reset_mock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    

    result_student = await student_repository.create(fake_student)

    assert result_user.username == "testCreate"
    assert result_student.user_id == 1
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()