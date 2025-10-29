"""
Roles Endpoint.

Defines the API routes for role operations such as creation, retrieval, 
updating, and deletion.

:author: Carlos S. Paredes Morillo
"""

from fastapi import APIRouter, Body, Depends, status
from fastapi.security import HTTPBearer
from dependency_injector.wiring import Provide, inject

from src.container import Container
from src.domain.objects.role.role_dto import RoleDTO
from src.infrastructure.controllers.role import RoleController


router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)

security = HTTPBearer()


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="all",
    summary="Get all roles",
    response_description="Returns a list of all roles",
)
@inject
async def get_roles(
    controller: RoleController = Depends(Provide[Container.role_controller])
):
    """Retrieve all roles in the system.

    Args:
        controller (RoleController): Controller handling role operations.

    Returns:
        list: List of RoleDTO objects.
    """
    return await controller.get_all()


@router.post(
    "/create-role",
    status_code=status.HTTP_200_OK,
    name="create-role",
    summary="Create a new role",
    response_description="Returns the created role ID and timestamp",
)
@inject
async def create_role(
    role_name: str = Body(..., embed=True),
    controller: RoleController = Depends(Provide[Container.role_controller])
):
    """Create a new role in the system.

    Args:
        role_name (str): Name of the role to create.
        controller (RoleController): Controller handling role operations.

    Returns:
        dict: Created role ID and timestamp.
    """
    return await controller.create_role(role_name)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-role",
    summary="Update an existing role",
    response_description="Returns the updated role ID and timestamp",
)
@inject
async def update_role(
    role: RoleDTO,
    controller: RoleController = Depends(Provide[Container.role_controller])
):
    """Update an existing role.

    Args:
        role (RoleDTO): Role update payload.
        controller (RoleController): Controller handling role operations.

    Returns:
        dict: Updated role ID and timestamp.
    """
    return await controller.update_role(role)


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
    name="delete-role",
    summary="Delete a role",
    response_description="Returns the deleted role ID and timestamp",
)
@inject
async def delete_role(
    role_id: int,
    controller: RoleController = Depends(Provide[Container.role_controller])
):
    """Delete a role from the system.

    Args:
        role_id (int): ID of the role to delete.
        controller (RoleController): Controller handling role operations.

    Returns:
        dict: Deleted role ID and deletion timestamp.
    """
    return await controller.deleterole(role_id)
