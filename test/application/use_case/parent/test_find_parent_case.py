
from unittest.mock import AsyncMock, MagicMock
import pytest
from fastapi import HTTPException, status

from src.application.use_case.parent.find_parent_case import FindParentCase
from src.application.use_case.user.find_user_case import FindUserCase
from src.domain.objects.profiles.parent_info import ParentDTO
from src.domain.objects.user.user_dto import UserDTO
from src.infrastructure.entities.users.parents import Parent
from src.infrastructure.repositories.parent import ParentRepository

@pytest.fixture
def mock_repo():
    return AsyncMock(spec=ParentRepository)

@pytest.fixture
def mock_find_user():
    return AsyncMock(spec=FindUserCase)

@pytest.fixture
def find_parent_case(mock_repo, mock_find_user):
    return FindParentCase(repo=mock_repo, find_user=mock_find_user)

@pytest.mark.asyncio
async def test_get_parent_success(find_parent_case, mock_repo, mock_find_user):
    user_id = 1


    parent_info = [MagicMock(student_id=101), MagicMock(student_id=102)]
    mock_repo.get.return_value = parent_info

    user = UserDTO(
        user_id=1,
        username="testuser",
        name="John",
        last_name="Doe",
        email="john@test.com",
        phone="123456789",
        dni="12345678A",
        role=2
    )
    mock_find_user.get_user_by_id.return_value = user

    result = await find_parent_case.get(user_id=user_id)

    assert isinstance(result, ParentDTO)
    assert result.user_id == user.user_id
    assert result.name == user.name
    assert result.last_name == user.last_name
    assert result.email == user.email
    assert result.phone == user.phone
    assert result.students == [101, 102]

    mock_repo.get.assert_awaited_once_with(user_id)
    mock_find_user.get_user_by_id.assert_awaited_once_with(user_id)

@pytest.mark.asyncio
async def test_get_parent_not_found_raises(find_parent_case, mock_repo):
    user_id = 1
    mock_repo.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await find_parent_case.get(user_id=user_id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Parent not found"
    mock_repo.get.assert_awaited_once_with(user_id)

@pytest.mark.asyncio
async def test_get_all_parents_success(find_parent_case, mock_repo):
    parent_list = [
        ParentDTO(user_id=1, name="John", last_name="Doe", email="a@test.com", phone="123", students=[101, 102]),
        ParentDTO(user_id=2, name="Jane", last_name="Doe", email="b@test.com", phone="456", students=[103])
    ]
    mock_repo.get_all.return_value = parent_list

    result = await find_parent_case.get_all()

    assert result == parent_list
    mock_repo.get_all.assert_awaited_once()

