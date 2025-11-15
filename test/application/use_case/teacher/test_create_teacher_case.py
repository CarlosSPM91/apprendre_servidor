import pytest
from unittest.mock import AsyncMock, MagicMock

from src.application.use_case.teacher.create_teacher_case import CreateTeacherCase
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.profiles.teacher_dto import TeacherDTO
from src.infrastructure.entities.users.teacher import Teacher


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def create_teacher_case(mock_repo):
    return CreateTeacherCase(repo=mock_repo)


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
async def test_create_teacher_success(create_teacher_case, mock_repo):
    mock_repo.create.return_value = MagicMock(id=1)

    result = await create_teacher_case.create(user_id=1)

    assert isinstance(result, CommonResponse)
    assert result.item_id == 1
    mock_repo.create.assert_awaited_once_with(user_id=1)
