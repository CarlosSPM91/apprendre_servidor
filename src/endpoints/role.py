
from fastapi import APIRouter, Body, Depends, status
from fastapi.security import HTTPBearer
from dependency_injector.wiring import Provide, inject

from src.container import Container
from src.domain.objects.role.role_dto import RoleDTO
from src.infrastructure.controllers.role import RoleController


router = APIRouter(
    prefix="/role",
    tags=["role"]
)

secutiry = HTTPBearer()

@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="all"
)
@inject
async def get_roles(
    controller: RoleController = Depends(Provide[Container.role_controller])
):
    return await controller.get_all()

@router.post(
    "/create-role",
    status_code=status.HTTP_200_OK,
    name="create-role"
)
@inject
async def create_role(
    role_name: str = Body(..., embed=True),
    controller: RoleController = Depends(Provide[Container.role_controller])
):
    return await controller.create_role(role_name)

@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-role"
)
@inject
async def update_role(
    role: RoleDTO,
    controller: RoleController = Depends(Provide[Container.role_controller])
):
    return await controller.update_role(role)

@router.delete(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
    name="delete-role"
)
@inject
async def delete_role(
    role_id: int,
    controller: RoleController = Depends(Provide[Container.role_controller])
):
    return await controller.deleterole(role_id)