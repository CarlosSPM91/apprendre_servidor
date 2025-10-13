import pytest
from unittest.mock import AsyncMock, Mock
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.application.services.token_service import TokenService
from src.middleware.token.authenticateToken import get_current_user, require_role


@pytest.fixture
def token_service():
    service = AsyncMock(spec=TokenService)
    service.decode_token.return_value = {"user_id": 1, "role": 2}
    service.validate_token.return_value = None
    service.get_user_info.return_value = {"user_id": 1, "role": 2}
    return service


@pytest.mark.asyncio
async def test_get_current_user_success(token_service):
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="fake_token")
    
    token_service = AsyncMock(spec=TokenService)
    token_service.decode_token.return_value = {"user_id": 1, "role": 2}
    token_service.validate_token.return_value = None
    token_service.get_user_info.return_value = {"user_id": 1, "role": 2}
    
    result = await get_current_user(credentials=credentials, token_service=token_service)
    
    token_service.decode_token.assert_called_once_with("fake_token")
    token_service.validate_token.assert_awaited_once()
    token_service.get_user_info.assert_awaited_once_with("fake_token")
    assert result["user_id"] == 1

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(token_service):
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="fake_token")
    
    token_service.validate_token.side_effect = HTTPException(status_code=401)
    
    with pytest.raises(HTTPException):
        await get_current_user(credentials=credentials, token_service=token_service)

@pytest.mark.asyncio
async def test_require_role_success(token_service):
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="fake_token")
    
    token_service.validate_token.return_value = Mock(role=2)
    role_checker = require_role(required_roles=[1, 2])
    result = await role_checker(credentials=credentials, token_service=token_service)
    
    assert result.role == 2

@pytest.mark.asyncio
async def test_require_role_insufficient(token_service):
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="fake_token")
    
    token_service.validate_token.return_value = Mock(role=3)
    role_checker = require_role(required_roles=[1, 2])
    
    with pytest.raises(HTTPException) as exc_info:
        await role_checker(credentials=credentials, token_service=token_service)
    
    assert exc_info.value.status_code == 403
