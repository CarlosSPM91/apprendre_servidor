from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
import pytest
from sqlalchemy import Select

from src.domain.objects.profiles.student_info_dto import StudentInfoDTO
from src.domain.objects.profiles.student_update_dto import StudentUpdateDTO
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance
from src.infrastructure.entities.student_info.medical_info import MedicalInfo
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
    return Student(id=1, user_id=1, observations="No observaciones")


@pytest.fixture
def fake_user():
    return User(
        id=1,
        username="testCreate",
        name="Test",
        last_name="Create",
        email="create@test.com",
        phone=123456,
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
        phone=123456,
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
async def test_get_student_full_info_succes(
    fake_student, fake_user, student_repository, mock_session
):

    fake_allergy = AllergyInfo(id=1, name="Peanuts")
    fake_intolerance = FoodIntolerance(id=2, name="Milk")
    fake_medical = MedicalInfo(id=3, name="Asma")

    mock_student_result = MagicMock()
    mock_student_result.first.return_value = (fake_student, fake_user)

    mock_allergies_result = MagicMock()
    mock_allergies_result.all.return_value = [fake_allergy]

    mock_intolerances_result = MagicMock()
    mock_intolerances_result.all.return_value = [fake_intolerance]

    mock_medical_result = MagicMock()
    mock_medical_result.all.return_value = [fake_medical]

    mock_session.exec = AsyncMock(
        side_effect=[
            mock_student_result,
            mock_allergies_result,
            mock_intolerances_result,
            mock_medical_result,
        ]
    )

    result = await student_repository.get_student_full_info(1)

    assert isinstance(result, StudentInfoDTO)
    assert result.student_id == 1
    assert result.user_id == 1
    assert result.name == "Test"
    assert result.last_name == "Create"
    assert result.email == "create@test.com"
    assert result.phone == 123456
    assert result.obvervations == "No observaciones"
    assert len(result.allergies) == 1
    assert result.allergies[0].name == "Peanuts"
    assert len(result.food_intolerance) == 1
    assert result.food_intolerance[0].name == "Milk"
    assert len(result.medical_info) == 1
    assert result.medical_info[0].name == "Asma"
    assert mock_session.exec.await_count == 4


@pytest.mark.asyncio
async def test_get_student_full_info_not_found(student_repository, mock_session):
    mock_result_select = MagicMock()
    mock_result_select.first = MagicMock(return_value=None)

    mock_session.exec = AsyncMock(return_value=mock_result_select)

    with pytest.raises(HTTPException) as exc_info:
        await student_repository.get_student_full_info(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Student not found"
    mock_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_student_success(fake_student, student_repository, mock_session):

    result = await student_repository.create(fake_student)

    assert result.user_id == 1
    assert result.observations == "No observaciones"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_user_and_student_success(
    fake_user_create_dto,
    fake_student,
    user_repository,
    student_repository,
    mock_session,
):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = None 

    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    
    result = await student_repository.create(fake_student)

    assert result.user_id == 1
    assert result.observations == "No observaciones"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_student_success(fake_student, student_repository, mock_session):

    mock_exists_result = MagicMock()
    mock_exists_result.first.return_value = None  

    mock_session.exec = AsyncMock(return_value=mock_exists_result)
    
    new_student = Student(
        user_id=fake_student.user_id,
        observations=fake_student.observations
    )
    
    result = await student_repository.create(new_student)

    assert result.user_id == 1
    assert result.observations == "No observaciones"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_student_already_exists(fake_student, student_repository, mock_session):

    mock_exists_result = MagicMock()
    mock_exists_result.first.return_value = fake_student
    
    mock_session.exec = AsyncMock(return_value=mock_exists_result)
    
    with pytest.raises(HTTPException) as exc_info:
        await student_repository.create(fake_student)
    
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Student already exist"
    mock_session.exec.assert_awaited_once()
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()

@pytest.mark.asyncio
async def test_update_student_not_found(student_repository, mock_session):
    update_student = StudentUpdateDTO(
        student_id=999,
        user_id=999,
        observations="Updated observations",
    )

    mock_result_select = MagicMock()
    mock_result_select.first = MagicMock(return_value=None)

    mock_session.exec = AsyncMock(return_value=mock_result_select)

    with pytest.raises(HTTPException) as exc_info:
        await student_repository.update(update_student)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Student not found"
    mock_session.exec.assert_awaited_once()
    mock_session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_delete_student_success(fake_student, student_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_exec_result.first = AsyncMock(return_value=fake_student)

    mock_session.exec = AsyncMock(return_value=mock_exec_result)

    result = await student_repository.delete(1)

    assert result is True
    mock_session.exec.assert_awaited()
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_student_not_found(student_repository, mock_session):
    mock_result_select = MagicMock()
    mock_result_select.first = MagicMock(return_value=None)

    mock_session.exec = AsyncMock(return_value=mock_result_select)
    mock_session.delete = AsyncMock()

    with pytest.raises(HTTPException) as exc_info:
        await student_repository.delete(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Student not found"
    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()
