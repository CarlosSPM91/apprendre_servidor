import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from src.application.use_case.role.delete_role_case import DeleteRoleCase
from src.infrastructure.repositories.role import RoleRepository
from src.domain.objects.common.common_resp import CommonResponse

@pytest.fixture
def role_repo():
    repo = AsyncMock()
    return repo

@pytest.fixture
def delete_role_case(role_repo):
    return DeleteRoleCase(role_repo)

@pytest.mark.asyncio
async def test_delete_role_success(delete_role_case, role_repo):
    role_id = 1

    result = await delete_role_case.delete(role_id)

    role_repo.delete.assert_awaited_once_with(role_id)

    assert isinstance(result, CommonResponse)
    assert result.item_id == role_id
    assert isinstance(result.event_date, datetime)
    assert result.event_date.tzinfo == timezone.utc
