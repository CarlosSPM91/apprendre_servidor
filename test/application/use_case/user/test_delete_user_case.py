from datetime import datetime, timezone
import pytest
from unittest.mock import AsyncMock, Mock
from fastapi import HTTPException
from src.application.services.password_service import PasswordService
from src.application.use_case.user.delete_user_case import DeleteUserCase
from src.application.use_case.user.update_user_case import UpdateUserCase
from src.domain.objects.auth.change_pass_dto import ChangePasswordDTO
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.entities.users.deletion_logs import DeletionLog
from src.infrastructure.repositories.user import UserRepository


@pytest.fixture
def user_repo():
    return AsyncMock()

@pytest.fixture
def deletion_repo():
    return AsyncMock()

@pytest.fixture
def find_user_case():
    mock = AsyncMock()
    mock.get_user_by_id = AsyncMock()
    return mock

@pytest.fixture
def use_case(user_repo, find_user_case, deletion_repo):
    return DeleteUserCase(user_repo, find_user_case, deletion_repo)

@pytest.mark.asyncio
async def test_delete_user_success(use_case, user_repo, find_user_case, deletion_repo):
    user_id = 1
    user_who_delete = 2

    mock_user = AsyncMock()
    mock_user.user_id = user_id
    mock_user.name = "Test"
    mock_user.last_name = "Ex"

    mock_eraser = AsyncMock()
    mock_eraser.user_id = user_who_delete
    mock_eraser.name = "Admin"
    mock_eraser.last_name = "Root"


    find_user_case.get_user_by_id.side_effect = [mock_user, mock_eraser]
    deletion_repo.create.return_value = None
    user_repo.delete.return_value = True

    resp = await use_case.delete(user_id, user_who_delete)

    assert find_user_case.get_user_by_id.await_count == 2
    deletion_repo.create.assert_awaited_once()
    user_repo.delete.assert_awaited_once_with(user_id)

    log_arg = deletion_repo.create.await_args.args[0]
    assert log_arg.user_id == user_id
    assert log_arg.user_who_deleted == user_who_delete

    assert isinstance(resp, CommonResponse)
    assert resp.item_id == user_id
    assert resp.event_date.tzinfo == timezone.utc