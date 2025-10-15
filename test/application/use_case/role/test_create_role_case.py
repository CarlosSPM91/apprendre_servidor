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

@pytest.fixture
def token_service():
    """
    @brief Fixture that creates a mock token service.
    @return AsyncMock with invalidate_token simulated.
    """
    mock = AsyncMock()
    mock.invalidate_token = AsyncMock()
    return mock

@pytest.fixture
def use_case(token_service):
    """
    @brief Fixture that instantiates LogoutUseCase with the mocked token_service.
    @param token_service Mock of the token service.
    @return Instance of LogoutUseCase.
    """
    return LogoutUseCase(token_service)

@pytest.mark.asyncio
async def test_logout_success(use_case, token_service):
    """
    @brief Verifies that logout calls invalidate_token and returns True on success.
    @param use_case Instance of LogoutUseCase.
    @param token_service Mock of the token service.
    """
    user_id = 123
    token_service.invalidate_token.return_value = True

    result = await use_case.logout(user_id)

    token_service.invalidate_token.assert_awaited_once_with(user_id)
    assert result is True

@pytest.mark.asyncio
async def test_logout_raises_error(use_case, token_service):
    """
    @brief Verifies that logout propagates the exception if invalidate_token fails.
    @param use_case Instance of LogoutUseCase.
    @param token_service Mock of the token service.
    """
    user_id = 456
    token_service.invalidate_token.side_effect = Exception("Token error")

    with pytest.raises(Exception) as exc_info:
        await use_case.logout(user_id)

    assert str(exc_info.value) == "Token error"
    token_service.invalidate_token.assert_awaited_once_with(user_id)

@pytest.mark.asyncio
async def test_logout_returns_false_when_invalidation_fails(use_case, token_service):
    """
    @brief Verifies that logout returns False if invalidate_token returns False.
    @param use_case Instance of LogoutUseCase.
    @param token_service Mock of the token service.
    """
    user_id = 789
    token_service.invalidate_token.return_value = False

    result = await use_case.logout(user_id)

    token_service.invalidate_token.assert_awaited_once_with(user_id)
    assert result is False

@pytest.mark.asyncio
async def test_logout_with_none_user_id(use_case, token_service):
    """
    @brief Verifies that logout raises TypeError when user_id is None.
    @param use_case Instance of LogoutUseCase.
    @param token_service Mock of the token service.
    """
    token_service.invalidate_token.return_value = True

    with pytest.raises(TypeError):
        await use_case.logout(None)

@pytest.mark.asyncio
async def test_logout_multiple_calls(use_case, token_service):
    """
    @brief Verifies that logout can be called multiple times with different user_ids.
    @param use_case Instance of LogoutUseCase.
    @param token_service Mock of the token service.
    """
    user_ids = [101, 202, 303]
    token_service.invalidate_token.return_value = True

    for user_id in user_ids:
        result = await use_case.logout(user_id)
        token_service.invalidate_token.assert_awaited_with(user_id)
        assert result is True
    assert token_service.invalidate_token.await_count == len(user_ids)
