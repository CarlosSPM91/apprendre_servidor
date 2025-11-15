import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, status
from datetime import datetime, timezone

from src.application.use_case.student.create_student_case import CreateStudenCase
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.profiles.student_update_dto import StudentUpdateDTO
from src.domain.objects.profiles.student_info_dto import StudentInfoDTO
from src.infrastructure.entities.student_info.student import Student



@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def create_student_case(mock_repo):
    return CreateStudenCase(repo=mock_repo)


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
async def test_create_student_success(create_student_case, mock_repo, sample_student):
    mock_repo.create.return_value = sample_student

    result = await create_student_case.create(sample_student)

    assert isinstance(result, CommonResponse)
    assert result.item_id == sample_student.id
    mock_repo.create.assert_awaited_once_with(sample_student)

