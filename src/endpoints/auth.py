
from typing import Container
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer

from src.container import Container
from dependency_injector.wiring import Provide
from src.domain.objects.auth.login_req import LoginRequest
from src.domain.objects.auth.login_resp import LoginResponse
from src.infrastructure.controllers.auth import AuthController


router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

secutiry = HTTPBearer()

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    name="login"
)
async def login(
    payload:LoginRequest,
    controller: AuthController = Depends(Provide[Container.auth_controller])
):
    return await controller.login(payload)