"""
Users Endpoint.

Defines the API routes for user operations (creation, retrieval, etc.).

:author: Carlos S. Paredes Morillo
"""
from fastapi import APIRouter, Depends, status

from src.container import Container
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.controllers.user import UserController
from dependency_injector.wiring import inject, Provide


router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    name="me",
)
@inject
async def me(
    controller: UserController = Depends(Provide[Container.user_controller])
):
    return await controller.me()

@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    name="find"
)
@inject
async def find_user(
    user_id: str,
    controller: UserController = Depends(Provide[Container.user_controller])
):
    return await controller.get_user(user_id)

@router.post(
    "/create-user",
    status_code=status.HTTP_201_CREATED,
    name="create-user"
)
@inject
async def create_user(
    payload: UserCreateDTO,
    controller: UserController = Depends(Provide[Container.user_controller])
):
    print("-----ENDPOINT----->"+(str(payload.role_id)))
    return await controller.create_user(payload)

@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-user"
)
@inject
async def update_user(
    payload: UserUpdateDTO,
    controller: UserController = Depends(Provide[Container.user_controller])
):
    return await controller.update_user(payload)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete-user"
)
@inject
async def delete_user(
    user_id:str,
    controller: UserController = Depends(Provide[Container.user_controller])
):
    return await controller.delete_user(user_id)