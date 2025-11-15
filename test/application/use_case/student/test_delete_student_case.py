import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, status
from datetime import datetime, timezone

from src.application.use_case.student.find_student_case import FindStudentCase
from src.application.use_case.student.delete_student_case import DeleteStudentCase
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
def delete_student_case(mock_repo, find_student_case):
    return DeleteStudentCase(repo=mock_repo, find_student_case=find_student_case)


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
async def test_delete_student_success(delete_student_case, mock_repo, sample_student):
    delete_student_case.find_case.get_student_by_id = AsyncMock(return_value=sample_student)
    mock_repo.delete.return_value = True

    result = await delete_student_case.delete(student_id=1)

    assert isinstance(result, CommonResponse)
    assert result.item_id == 1
    delete_student_case.find_case.get_student_by_id.assert_awaited_once_with(1)
    mock_repo.delete.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_delete_student_not_found_raises(delete_student_case, mock_repo):
    delete_student_case.find_case.get_student_by_id = AsyncMock(side_effect=HTTPException(status_code=404))

    with pytest.raises(HTTPException):
        await delete_student_case.delete(student_id=999)
