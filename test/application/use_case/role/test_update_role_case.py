"""
@file test_update_role_case.py
@brief Unit tests for UpdateRoleCase.
@details This file contains tests for the UpdateRoleCase class, verifying correct behavior for role updates and response formatting.
"""

import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from src.application.use_case.role.update_role_case import UpdateRoleCase
from src.infrastructure.repositories.role import RoleRepository
from src.domain.objects.role.role_dto import RoleDTO
from src.domain.objects.common.common_resp import CommonResponse

@pytest.fixture
def role_repo():
    """
    @brief Fixture that creates a mock RoleRepository.
    @return AsyncMock instance of RoleRepository.
    """
    return AsyncMock()

@pytest.fixture
def update_role_case(role_repo):
    """
    @brief Fixture that instantiates UpdateRoleCase with the mocked RoleRepository.
    @param role_repo Mocked RoleRepository.
    @return Instance of UpdateRoleCase.
    """
    return UpdateRoleCase(role_repo)

@pytest.mark.asyncio
async def test_update_role_success(update_role_case, role_repo):
    """
    @brief Verifies that update_role_case.update returns a valid CommonResponse on success.
    @param update_role_case Instance of UpdateRoleCase.
    @param role_repo Mocked RoleRepository.
    """
    role_update = RoleDTO(role_id=1, role_name="Admin")

    role_repo.update_role.return_value = role_update
    result = await update_role_case.update(role_update)

    role_repo.update_role.assert_awaited_once_with(role_update)

    assert isinstance(result, CommonResponse)
    assert result.item_id == role_update.role_id
    assert isinstance(result.event_date, datetime)
    assert result.event_date.tzinfo == timezone.utc
