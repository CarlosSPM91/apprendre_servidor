
from fastapi import APIRouter, Depends, status

from src.container import Container
from dependency_injector.wiring import Provide, inject
from src.domain.objects.auth.login_req import LoginRequest
from src.domain.objects.auth.login_resp import LoginResponse
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.auth import AuthController
from src.middleware.token.authenticateToken import get_current_user, get_token


router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)
@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    name="login"
)
@inject
async def login(
    payload:LoginRequest,
    controller: AuthController = Depends(Provide[Container.auth_controller])
):
    return await controller.login(payload)

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    name="logout"
)
@inject
async def logout(
    controller: AuthController = Depends(Provide[Container.auth_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    return await controller.logout(current_user.user_id)