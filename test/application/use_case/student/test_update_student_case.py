import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, status
from datetime import datetime, timezone


from src.application.use_case.student.update_student_case import UpdateStudentCase
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.profiles.student_update_dto import StudentUpdateDTO
from src.domain.objects.profiles.student_info_dto import StudentInfoDTO
from src.infrastructure.entities.student_info.student import Student



@pytest.fixture
def mock_repo():
    return AsyncMock()

@pytest.fixture
def update_student_case(mock_repo):
    return UpdateStudentCase(repo=mock_repo)



@pytest.fixture
def sample_student():
    return Student(id=1, user_id=1, observations="test")


@pytest.fixture
def student_update_dto():
    return StudentUpdateDTO(student_id=1, observations="updated")


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
async def test_update_student_success(update_student_case, mock_repo, student_update_dto, sample_student):
    mock_repo.update.return_value = sample_student

    result = await update_student_case.update_student(student_update_dto)

    assert isinstance(result, CommonResponse)
    assert result.item_id == sample_student.id
    mock_repo.update.assert_awaited_once_with(student_update_dto)

