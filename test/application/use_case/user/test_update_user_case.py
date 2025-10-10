from datetime import datetime, timezone
import pytest
from unittest.mock import AsyncMock, Mock
from fastapi import HTTPException
from src.application.services.password_service import PasswordService
from src.application.use_case.user.update_user_case import UpdateUserCase
from src.domain.objects.auth.change_pass_dto import ChangePasswordDTO
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.repositories.user import UserRepository


@pytest.fixture
def repo():
    return AsyncMock(spec=UserRepository)

@pytest.fixture
def pwd_service():
    return Mock(spec=PasswordService)

@pytest.fixture
def use_case(repo, pwd_service):
    return UpdateUserCase(pwd_service, repo)

@pytest.mark.asyncio
async def test_update_user_success(use_case, repo):
    user_dto = UserUpdateDTO(
        user_id=1,
        name="Test",
        last_name="User",
        username="testuser",
        dni="12345678A",
        email="test@example.com",
        phone=123456789,
        role_id=1,
        password="pass123"
    )
    repo.update_user.return_value = user_dto

    resp = await use_case.update_user(user_dto)

    assert isinstance(resp, CommonResponse)
    assert resp.item_id == user_dto.user_id
    assert isinstance(resp.event_date, datetime)
    assert resp.event_date.tzinfo == timezone.utc

    repo.update_user.assert_awaited_once_with(user_dto)

@pytest.mark.asyncio
async def test_update_last_used_success(use_case, repo):
    repo.update_last_used.return_value = True
    user_id = 1

    resp = await use_case.update_last_used(user_id)
    assert isinstance(resp, CommonResponse)
    assert resp.item_id == user_id
    assert isinstance(resp.event_date, datetime)
    assert resp.event_date.tzinfo == timezone.utc
    repo.update_last_used.assert_awaited_once_with(user_id)


@pytest.mark.asyncio
async def test_change_password_success(use_case, repo, pwd_service):
    payload = ChangePasswordDTO(user_id=1, password="newpass")

    pwd_service.hash_password.return_value = "hashed_pass"
    repo.change_password.return_value = True

    resp = await use_case.change_password(payload)

    pwd_service.hash_password.assert_called_once_with(payload.password)
    repo.change_password.assert_awaited_once_with(payload.user_id, "hashed_pass")
    assert isinstance(resp, CommonResponse)
    assert resp.item_id == payload.user_id
    assert isinstance(resp.event_date, datetime)
    assert resp.event_date.tzinfo == timezone.utc