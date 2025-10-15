
from unittest.mock import AsyncMock, MagicMock, Mock
import pytest

from src.infrastructure.entities.student_info.student import Student
from src.infrastructure.entities.users.user import User
from src.infrastructure.repositories.student import StudentRepository
from src.infrastructure.repositories.user import UserRepository



@pytest.fixture
def mock_session():
    return AsyncMock()

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

@pytest.mark.asyncio
async def test_init():
    mock_session_test = MagicMock()
    student_repository = StudentRepository(mock_session_test)
    assert student_repository.session == mock_session_test

@pytest.mark.asyncio
async def test_get_student_succes(fake_student,student_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = fake_student
    mock_session.exec.return_value = mock_exec_result
    print(fake_student)

    result= await student_repository.getStudent(1)
    print(result)

    assert result == fake_student
    assert result.id==1
    assert result.user_id==1

@pytest.mark.asyncio
async def test_get_student_full_info_succes(fake_student,student_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = fake_student
    mock_session.exec.return_value = mock_exec_result
    print(fake_student)

    result= await student_repository.getStudent(1)
    print(result)
    
    assert result == fake_student
    assert result.id==1
    assert result.user_id==1

@pytest.mark.asyncio
async def test_create_student_succes(fake_student,student_repository, mock_session):
    pass