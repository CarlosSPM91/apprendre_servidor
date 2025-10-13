"""
Authentication Endpoint.

Defines the API routes for authentication operations such as login and logout.

:author: Carlos S. Paredes Morillo
"""

from fastapi import APIRouter, Depends, status
from src.container import Container
from dependency_injector.wiring import Provide, inject
from src.domain.objects.auth.login_req import LoginRequest
from src.domain.objects.auth.login_resp import LoginResponse
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.auth import AuthController
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    name="login",
    summary="User login",
    response_description="Returns access token and user info",
)
@inject
async def login(
    payload: LoginRequest,
    controller: AuthController = Depends(Provide[Container.auth_controller])
):
    """Authenticate a user and generate a JWT token.

    Args:
        payload (LoginRequest): Login credentials (username & password).
        controller (AuthController): Controller handling authentication.

    Returns:
        LoginResponse: Contains access token, token type, user ID, username, and role.
    """
    return await controller.login(payload)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    name="logout",
    summary="User logout",
    response_description="Invalidates the current user's JWT token",
)
@inject
async def logout(
    controller: AuthController = Depends(Provide[Container.auth_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """Invalidate the current user's token (logout).

    Args:
        controller (AuthController): Controller handling authentication.
        current_user (JwtPayload): Currently authenticated user (from token).

    Returns:
        dict: Status message indicating success of logout.
    """
    return await controller.logout(current_user.user_id)
