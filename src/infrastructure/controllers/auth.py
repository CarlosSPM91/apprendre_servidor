"""
Authentication Controller.

Handles user authentication operations such as login and logout.
Integrates with LoginUseCase and LogoutUseCase for business logic,
and captures exceptions with Sentry.

:author: Carlos S. Paredes Morillo
"""

from fastapi import HTTPException, status
import sentry_sdk
from src.application.use_case.auth.login_use_case import LoginUseCase
from src.application.use_case.auth.logout_use_case import LogoutUseCase
from src.domain.exceptions.except_manager import manage_auth_except
from src.domain.objects.auth.login_req import LoginRequest


class AuthController:
    """Controller for authentication endpoints."""

    def __init__(self, login_case: LoginUseCase, logout_case: LogoutUseCase):
        """
        Initialize the AuthController with the required use cases.

        Args:
            login_case (LoginUseCase): Use case handling login logic.
            logout_case (LogoutUseCase): Use case handling logout logic.
        """
        self.login_case = login_case
        self.logout_case = logout_case

    async def login(self, payload: LoginRequest):
        """
        Authenticate a user with username and password.

        Args:
            payload (LoginRequest): Login request data including username and password.

        Returns:
            dict: Authentication result containing access token and user info.

        Raises:
            HTTPException: If login fails, exceptions are captured and managed.
        """
        try:
            return await self.login_case.login(payload)
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_auth_except(e)

    async def logout(self, token: str):
        """
        Invalidate a user's token and log out.

        Args:
            token (str): JWT token to invalidate.

        Returns:
            dict: Status message indicating session closure.

        Raises:
            HTTPException: If logout fails or token cannot be invalidated.
        """
        try:
            is_invalidated = await self.logout_case.logout(token)
            if not is_invalidated:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={"message": "Something went wrong"}
                )
            return {
                "status": "success",
                "message": "Session closed"
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_auth_except(e)
