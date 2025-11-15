import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, status
from datetime import datetime, timezone


from src.application.use_case.student.find_student_case import FindStudentCase
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.profiles.student_info_dto import StudentInfoDTO
from src.infrastructure.entities.student_info.student import Student



@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def find_student_case(mock_repo):
    return FindStudentCase(repo=mock_repo)


@pytest.fixture
def sample_student():
    return Student(id=1, user_id=1, observations="test")


@pytest.fixture
def sample_student_info_dto():
    return StudentInfoDTO(
        student_id=1,
        user_id=1,
        name="John",
        last_name="Doe",
        email="a@test.com",
        phone="123",
        username="johndoe",
        observations="test",
        allergies=[],
        medical_info=[],
        food_intolerance=[],
        classe="1A",
        dni="12345678A"
    )


@pytest.mark.asyncio
async def test_get_student_by_id_success(find_student_case, mock_repo, sample_student):
    mock_repo.get_student.return_value = sample_student

    result = await find_student_case.get_student_by_id(student_id=1)

    assert result == sample_student
    mock_repo.get_student.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_student_by_id_not_found(find_student_case, mock_repo):
    mock_repo.get_student.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await find_student_case.get_student_by_id(student_id=1)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Student not found"


@pytest.mark.asyncio
async def test_get_all_students(find_student_case, mock_repo, sample_student):
    mock_repo.get_all.return_value = [sample_student]

    result = await find_student_case.get_all()

    assert result == [sample_student]
    mock_repo.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_student_full_info_success(find_student_case, mock_repo, sample_student_info_dto):
    mock_repo.get_student_full_info.return_value = sample_student_info_dto

    result = await find_student_case.get_student_full_info(student_id=1)

    assert result == sample_student_info_dto
    mock_repo.get_student_full_info.assert_awaited_once_with(student_id=1)


@pytest.mark.asyncio
async def test_get_student_full_info_not_found(find_student_case, mock_repo):
    mock_repo.get_student_full_info.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await find_student_case.get_student_full_info(student_id=1)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Student not found"

