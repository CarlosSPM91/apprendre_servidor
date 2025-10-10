import pytest
from unittest.mock import AsyncMock
from src.application.use_case.auth.logout_use_case import LogoutUseCase


@pytest.fixture
def token_service():
    mock = AsyncMock()
    mock.invalidate_token = AsyncMock()
    return mock


@pytest.fixture
def use_case(token_service):
    return LogoutUseCase(token_service)


@pytest.mark.asyncio
async def test_logout_success(use_case, token_service):
    user_id = 123
    token_service.invalidate_token.return_value = True

    result = await use_case.logout(user_id)

    token_service.invalidate_token.assert_awaited_once_with(user_id)
    assert result is True



@pytest.mark.asyncio
async def test_logout_raises_error(use_case, token_service):
    user_id = 456
    token_service.invalidate_token.side_effect = Exception("Token error")

    with pytest.raises(Exception) as exc_info:
        await use_case.logout(user_id)

    assert str(exc_info.value) == "Token error"
    token_service.invalidate_token.assert_awaited_once_with(user_id)
