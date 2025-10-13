import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from src.application.use_case.role.update_role_case import UpdateRoleCase
from src.infrastructure.repositories.role import RoleRepository
from src.domain.objects.role.role_dto import RoleDTO
from src.domain.objects.common.common_resp import CommonResponse

@pytest.fixture
def role_repo():
    return AsyncMock()

@pytest.fixture
def update_role_case(role_repo):
    return UpdateRoleCase(role_repo)

@pytest.mark.asyncio
async def test_update_role_success(update_role_case, role_repo):
    role_update = RoleDTO(role_id=1, role_name="Admin")

    role_repo.update_role.return_value = role_update
    result = await update_role_case.update(role_update)

    role_repo.update_role.assert_awaited_once_with(role_update)

    assert isinstance(result, CommonResponse)
    assert result.item_id == role_update.role_id
    assert isinstance(result.event_date, datetime)
    assert result.event_date.tzinfo == timezone.utc
