import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, status
from datetime import datetime, timezone

from src.application.use_case.teacher.find_teacher_case import FindTeacherCase
from src.application.use_case.teacher.delete_teacher_case import DeleteTeacherCase

from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.profiles.teacher_dto import TeacherDTO
from src.infrastructure.entities.users.teacher import Teacher




@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def find_teacher_case(mock_repo):
    return FindTeacherCase(repo=mock_repo)


@pytest.fixture
def delete_teacher_case(mock_repo, find_teacher_case):
    return DeleteTeacherCase(repo=mock_repo, find_case=find_teacher_case)


@pytest.fixture
def sample_teacher():
    return Teacher(id=1, user_id=1)


@pytest.fixture
def sample_teacher_dto():
    return TeacherDTO(
        id=1,
        user_id=1,
        name="John",
        last_name="Doe",
        email="a@test.com",
        phone="123",
        username="johndoe"
    )


@pytest.mark.asyncio
async def test_delete_teacher_success(delete_teacher_case, mock_repo, sample_teacher):
    delete_teacher_case.find_case.get = AsyncMock(return_value=sample_teacher)
    mock_repo.delete.return_value = True

    result = await delete_teacher_case.delete(teacher_id=1)

    assert isinstance(result, CommonResponse)
    assert result.item_id == 1
    delete_teacher_case.find_case.get.assert_awaited_once_with(1)
    mock_repo.delete.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_delete_teacher_not_found_raises(delete_teacher_case, mock_repo):
    delete_teacher_case.find_case.get = AsyncMock(side_effect=HTTPException(status_code=404))

    with pytest.raises(HTTPException):
        await delete_teacher_case.delete(teacher_id=999)

