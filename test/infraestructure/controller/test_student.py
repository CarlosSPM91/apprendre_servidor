import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from datetime import datetime, timezone

from src.domain.objects.profiles.student_info_dto import StudentInfoDTO
from src.domain.objects.profiles.student_update_dto import StudentUpdateDTO
from src.infrastructure.controllers.student import StudentController
from src.infrastructure.entities.student_info.student import Student


@pytest.fixture
def create_case():
    mock = AsyncMock()
    return mock


@pytest.fixture
def update_case():
    mock = AsyncMock()
    return mock


@pytest.fixture
def delete_case():
    mock = AsyncMock()
    return mock


@pytest.fixture
def find_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def student_dto():
    return Student(
        id=1,
        user_id=1,
        observations="Test observations",
    )

@pytest.fixture
def student_update_dto():
    return StudentUpdateDTO(
        student_id=1,
        observations="Updated observations",
    )


@pytest.fixture
def student_controller(find_case, create_case, update_case, delete_case):
    return StudentController(
        find_case=find_case,
        create_case=create_case,
        update_case=update_case,
        delete_case=delete_case,
    )

@pytest.mark.asyncio
async def test_create_student_success(student_controller, create_case, student_dto):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)
    create_case.create.return_value = mock_response

    response = await student_controller.create(user_id=1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "created_date" in response["data"]
    create_case.create.assert_awaited_once_with(user_id=1)

@pytest.mark.asyncio
async def test_update_student_success(student_controller, update_case, find_case, student_update_dto):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)
    find_case.get_student_by_id.return_value = student_dto
    update_case.update_student.return_value = mock_response

    response = await student_controller.update(student_update_dto)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "updated_date" in response["data"]
    find_case.get_student_by_id.assert_awaited_once_with(student_id=student_update_dto.student_id)
    update_case.update_student.assert_awaited_once_with(student_update_dto)

@pytest.mark.asyncio
async def test_delete_student_success(student_controller, delete_case, find_case):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)
    find_case.get_student_by_id.return_value = MagicMock(id=1)
    delete_case.delete.return_value = mock_response

    response = await student_controller.delete(1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "deletion_date" in response["data"]
    find_case.get_student_by_id.assert_awaited_once_with(student_id=1)
    delete_case.delete.assert_awaited_once_with(student_id=1)

@pytest.mark.asyncio
async def test_get_student_success(student_controller, find_case, student_dto):
    find_case.get_student_by_id.return_value = student_dto

    response = await student_controller.get_student(student_id="1")

    assert response["data"] == student_dto
    find_case.get_student_by_id.assert_awaited_once_with(student_id="1")

@pytest.mark.asyncio
async def test_create_student_exception(student_controller, create_case):
    create_case.create.side_effect = HTTPException(status_code=400, detail="Error creating student")

    with pytest.raises(HTTPException):
        await student_controller.create(user_id=1)
    create_case.create.assert_awaited_once_with(user_id=1)

@pytest.mark.asyncio
async def test_update_student_exception(student_controller, update_case, find_case, student_update_dto):
    find_case.get_student_by_id.side_effect = HTTPException(status_code=404, detail="Student not found")

    with pytest.raises(HTTPException):
        await student_controller.update(payload=student_update_dto)
    find_case.get_student_by_id.assert_awaited_once_with(student_id=student_update_dto.student_id)
    update_case.update_student.assert_not_awaited()

@pytest.mark.asyncio
async def test_delete_student_exception(student_controller, delete_case, find_case):
    find_case.get_student_by_id.side_effect = HTTPException(status_code=404, detail="Student not found")

    with pytest.raises(HTTPException):
        await student_controller.delete(student_id=999)
    find_case.get_student_by_id.assert_awaited_once_with(student_id=999)
    delete_case.delete.assert_not_awaited()

@pytest.mark.asyncio
async def test_get_student_exception(student_controller, find_case):
    find_case.get_student_by_id.side_effect = HTTPException(status_code=404, detail="Student not found")

    with pytest.raises(HTTPException):
        await student_controller.get_student(student_id="999")
    find_case.get_student_by_id.assert_awaited_once_with(student_id="999")

@pytest.mark.asyncio
async def test_get_student_full_info_success(student_controller, find_case):
    student_info = StudentInfoDTO(
        student_id=1,
        user_id=1,
        observations="test observations",
        email="asd",
        classe="asd",
        name="test",
        last_name="last name",
        dni="12345678A",
        phone=123456789,
        username="testuser",
        allergies=[],
        medical_info=[],
        food_intolerance=[],
    )
    find_case.get_student_full_info.return_value = student_info

    response = await student_controller.get_student_full_info(student_id=1)

    assert response["data"] == student_info
    find_case.get_student_full_info.assert_awaited_once_with(student_id=1) 

@pytest.mark.asyncio
async def test_get_student_full_info_exception(student_controller, find_case):
    find_case.get_student_full_info.side_effect = HTTPException(status_code=404, detail="Student not found")

    with pytest.raises(HTTPException):
        await student_controller.get_student_full_info(student_id=999)
    find_case.get_student_full_info.assert_awaited_once_with(student_id=999)
    find_case.delete.assert_not_awaited()

@pytest.mark.asyncio
async def test_get_all_students_success(student_controller, find_case, fake_student):
    # Arrange
    find_case.get_all.return_value = [fake_student]

    # Act
    resp = await student_controller.get_all()

    # Assert
    assert resp["status"] == "success"
    assert len(resp["data"]) == 1
    assert resp["data"][0].username == fake_student.username
    find_case.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_students_success(student_controller, find_case):
    fake_student = MagicMock()
    fake_student.username = "testuser"

    find_case.get_all.return_value = [fake_student]

    response = await student_controller.get_all()

    assert response["status"] == "success"
    assert len(response["data"]) == 1
    assert response["data"][0].username == "testuser"
    find_case.get_all.assert_awaited_once()
