import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from src.domain.objects.user.user_dto import UserDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.repositories.acces_logs import AccessRepository
from src.infrastructure.repositories.user import UserRepository
from src.application.use_case.user.find_user_case import FindUserCase



@pytest.fixture
def repo():
    return AsyncMock(spec=UserRepository)

@pytest.fixture
def repo_access_logs():
    return AsyncMock(spec=AccessRepository)

@pytest.fixture
def use_case(repo, repo_access_logs):
    return FindUserCase(repo, repo_access_logs)

@pytest.mark.asyncio
async def test_get_user_by_username_found(use_case, repo):
    mock_user = UserUpdateDTO(
        user_id=1,
        name="test",
        last_name="Exemple",
        username="test",
        dni="00011122Z",
        email="maria@test.com",
        phone=999999,
        role_id=1,
        password="pass",
    )
    repo.get_user_by_username.return_value = mock_user

    result = await use_case.get_user_by_username("test")
    assert result == mock_user
    repo.get_user_by_username.assert_awaited_once_with("test")

@pytest.mark.asyncio
async def test_get_user_by_username_not_found(use_case, repo):
    repo.get_user_by_username.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        await use_case.get_user_by_username("test")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"

@pytest.mark.asyncio
async def test_get_user_by_id_found(use_case, repo):
    mock_user = UserUpdateDTO(
        user_id=1,
        name="test",
        last_name="Exemple",
        username="test",
        dni="00011122Z",
        email="maria@test.com",
        phone=999999,
        role_id=1,
        password="pass",
    )
    repo.get_user_by_id.return_value = mock_user

    result = await use_case.get_user_by_id(1)
    assert result == mock_user
    repo.get_user_by_id.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_get_user_by_id_not_found(use_case, repo):
    repo.get_user_by_id.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        await use_case.get_user_by_id(1)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"

@pytest.mark.asyncio
async def test_get_all_found(use_case, repo):
    mock_users = [
        UserDTO(user_id=1, username="user1", email="user1@test.com", name="Test1", last_name="User1", role=1),
        UserDTO(user_id=2, username="user2", email="user2@test.com", name="Test2", last_name="User2", role=2),
    ]
    repo.get_all.return_value = mock_users

    result = await use_case.get_all()
    assert result == mock_users
    repo.get_all.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_all_not_found(use_case, repo):
    repo.get_all.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        await use_case.get_all()
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Users not found"
