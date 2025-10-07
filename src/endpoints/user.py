"""
Users Endpoint.

Defines the API routes for user operations (creation, retrieval, etc.).

:author: Carlos S. Paredes Morillo
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.container import Container
from src.domain.objects.auth.change_pass_dto import ChangePasswordDTO
from src.domain.objects.token.jwtPayload import JwtPayload
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.controllers.user import UserController
from dependency_injector.wiring import inject, Provide

from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    name="me",
)
@inject
async def me(
    controller: UserController = Depends(Provide[Container.user_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    return await controller.me(current_user.user_id)


@router.get("/all", status_code=status.HTTP_200_OK, name="findAll")
@inject
async def find_all_user(
    current_user: JwtPayload = Depends(get_current_user),
    controller: UserController = Depends(Provide[Container.user_controller]),
):
    return await controller.get_all()


@router.get("/{user_id}/find", status_code=status.HTTP_200_OK, name="find")
@inject
async def find_user(
    user_id: int,
    controller: UserController = Depends(Provide[Container.user_controller]),
):
    return await controller.get_user(user_id)


@router.post("/create-user", status_code=status.HTTP_201_CREATED, name="create-user")
@inject
async def create_user(
    payload: UserCreateDTO,
    controller: UserController = Depends(Provide[Container.user_controller]),
):
    return await controller.create_user(payload)


@router.put("/", status_code=status.HTTP_200_OK, name="update-user")
@inject
async def update_user(
    payload: UserUpdateDTO,
    controller: UserController = Depends(Provide[Container.user_controller]),
):
    return await controller.update_user(payload)


@router.put("/change-password", status_code=status.HTTP_200_OK, name="change-password")
@inject
async def change_password(
    payload: ChangePasswordDTO,
    controller: UserController = Depends(Provide[Container.user_controller]),
):
    return await controller.change_password(payload)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, name="delete-user")
@inject
async def delete_user(
    user_id: int,
    controller: UserController = Depends(Provide[Container.user_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    return await controller.delete_user(user_id, current_user.user_id)
