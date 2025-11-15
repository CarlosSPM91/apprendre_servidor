import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException, status

from src.application.use_case.teacher.find_teacher_case import FindTeacherCase
from src.domain.objects.profiles.teacher_dto import TeacherDTO
from src.infrastructure.entities.users.teacher import Teacher



@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def find_teacher_case(mock_repo):
    return FindTeacherCase(repo=mock_repo)



@pytest.fixture
def sample_teacher():
    return Teacher(id=1, user_id=1)


@pytest.fixture
def sample_teacher_dto():
    return TeacherDTO(
        id=1,
        user_id=1,
        teacher_id=1,
        name="John",
        last_name="Doe",
        email="a@test.com",
        phone="123",
        username="johndoe"
    )

@pytest.mark.asyncio
async def test_find_teacher_success(find_teacher_case, mock_repo, sample_teacher):
    mock_repo.get_teacher.return_value = sample_teacher

    result = await find_teacher_case.get(student_id=1)

    assert result == sample_teacher
    mock_repo.get_teacher.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_find_teacher_not_found_raises(find_teacher_case, mock_repo):
    mock_repo.get_teacher.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await find_teacher_case.get(student_id=1)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Teacher not found"


@pytest.mark.asyncio
async def test_get_all_teachers_success(find_teacher_case, mock_repo, sample_teacher_dto):
    mock_repo.get_all.return_value = [sample_teacher_dto]

    result = await find_teacher_case.get_all()

    assert result == [sample_teacher_dto]
    mock_repo.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_teachers_not_found_raises(find_teacher_case, mock_repo):
    mock_repo.get_all.return_value = None

    with pytest.raises(HTTPException):
        await find_teacher_case.get_all()


@pytest.mark.asyncio
async def test_get_teacher_full_info_success(find_teacher_case, mock_repo, sample_teacher_dto):
    mock_repo.get_teacher_full_info.return_value = sample_teacher_dto

    result = await find_teacher_case.get_teacher_full_info(teacher_id=1)

    assert result == sample_teacher_dto
    mock_repo.get_teacher_full_info.assert_awaited_once_with(teacher_id=1)


@pytest.mark.asyncio
async def test_get_teacher_full_info_not_found_raises(find_teacher_case, mock_repo):
    mock_repo.get_teacher_full_info.return_value = None

    with pytest.raises(HTTPException):
        await find_teacher_case.get_teacher_full_info(teacher_id=1)

