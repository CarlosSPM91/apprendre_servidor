import pytest
from unittest.mock import AsyncMock, Mock
from fastapi import HTTPException, status
from datetime import datetime, timezone
from unittest.mock import patch

from src.infrastructure.controllers.auth import AuthController
from src.application.use_case.auth.login_use_case import LoginUseCase
from src.application.use_case.auth.logout_use_case import LogoutUseCase
from src.domain.objects.auth.login_req import LoginRequest


@pytest.fixture
def login_case():
    return AsyncMock(spec=LoginUseCase)

@pytest.fixture
def logout_case():
    return AsyncMock(spec=LogoutUseCase)

@pytest.fixture
def auth_controller(login_case, logout_case):
    return AuthController(login_case=login_case, logout_case=logout_case)


@pytest.mark.asyncio
async def test_login_success(auth_controller, login_case):
    payload = LoginRequest(username="user", password="pass")
    login_case.login.return_value = {
        "access_token": "fake_token",
        "token_type": "bearer",
        "user_id": "1",
        "username": "user",
        "role": 1
    }

    resp = await auth_controller.login(payload)

    assert resp["access_token"] == "fake_token"
    login_case.login.assert_awaited_once_with(payload)


@pytest.mark.asyncio
async def test_login_exception(auth_controller, login_case):
    payload = LoginRequest(username="user", password="pass")
    login_case.login.side_effect = HTTPException(status_code=401, detail="Invalid")

    with patch("src.infrastructure.controllers.auth.sentry_sdk.capture_exception") as mock_sentry, \
         patch("src.infrastructure.controllers.auth.manage_auth_except") as mock_manager:

        await auth_controller.login(payload)

        login_case.login.assert_awaited_once_with(payload)
        mock_sentry.assert_called()
        mock_manager.assert_called()


@pytest.mark.asyncio
async def test_logout_success(auth_controller, logout_case):
    token = "fake_token"
    logout_case.logout.return_value = True

    resp = await auth_controller.logout(token)

    assert resp["status"] == "success"
    assert resp["message"] == "Session closed"
    logout_case.logout.assert_awaited_once_with(token)


@pytest.mark.asyncio
async def test_logout_failure(auth_controller, logout_case):
    token = "fake_token"
    logout_case.logout = AsyncMock(return_value=False)

    with patch("src.infrastructure.controllers.auth.sentry_sdk.capture_exception") as mock_sentry, \
         patch("src.infrastructure.controllers.auth.manage_auth_except") as mock_manager:

        result = await auth_controller.logout(token)

        assert result is None
        mock_sentry.assert_called()
        mock_manager.assert_called()