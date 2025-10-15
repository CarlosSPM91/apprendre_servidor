import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from src.application.use_case.role.create_role_case import CreateRoleCase
from src.infrastructure.repositories.role import RoleRepository
from src.domain.objects.common.common_resp import CommonResponse

"""
@file test_logout_case.py
@brief Unit tests for LogoutUseCase.
@details This file contains tests for the LogoutUseCase class, verifying correct behavior for token invalidation during logout.
"""

@pytest.fixture
def role_repo():
    repo = AsyncMock()
    return repo

@pytest.fixture
def create_role_case(role_repo):
    return CreateRoleCase(role_repo)

@pytest.mark.asyncio
async def test_create_role_success(create_role_case, role_repo):
    mock_role = AsyncMock()
    mock_role.role_id = 1
    role_repo.create.return_value = mock_role

    role_name = "Admin"
    result = await create_role_case.create(role_name)

    role_repo.create.assert_awaited_once_with(role_name)
    assert isinstance(result, CommonResponse)
    assert result.item_id == 1
    assert isinstance(result.event_date, datetime)
    assert result.event_date.tzinfo == timezone.utc
