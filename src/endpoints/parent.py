
from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.parent import ParentController
from src.infrastructure.entities.users.parents import Parent
from src.middleware.token.authenticateToken import get_current_user, require_role

"""
Parents Endpoints.

Provides API routes for managing Parent entities.

:author: Carlos S. Paredes Morillo
"""


router = APIRouter(prefix="/parents", tags=["parents"])

@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find-all-parents",
    summary="Get all parents",
    response_description="Returns a list of all parents",
)
@inject
async def find_all(
    current_user: JwtPayload = Depends(get_current_user),
    controller: ParentController = Depends(Provide[Container.parent_controller]),
):
    """
    Retrieve all parents with their associated students.

    Args:
        current_user (JwtPayload): The authenticated user.
        controller (ParentController): Controller to handle business logic.

    Returns:
        List[ParentDTO]: List of parents with their students.

    Raises:
        HTTPException: If no parents found or a database error occurs.
    """
    return await controller.get_all()


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    name="find-parent",
    summary="Get information of a parent",
    response_description="Returns the information of the parent",
)
@inject
async def find(
    user_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: ParentController = Depends(Provide[Container.parent_controller]),
):
    """
    Retrieve a parent by user ID.

    Args:
        user_id (int): The parent's user ID.
        current_user (JwtPayload): The authenticated user.
        controller (ParentController): Controller to handle business logic.

    Returns:
        List[Parent]: Parent entity/entities.

    Raises:
        HTTPException: If parent not found or retrieval fails.
    """
    return await controller.get_parent(user_id=user_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create-parent",
    summary="Create a parent",
    response_description="Returns the created parent",
)
@inject
async def create(
    payload: Parent,
    current_user: JwtPayload = Depends(get_current_user),
    controller: ParentController = Depends(Provide[Container.parent_controller]),
):
    """
    Create a new parent.

    Args:
        payload (Parent): The parent entity to create.
        current_user (JwtPayload): The authenticated user.
        controller (ParentController): Controller to handle business logic.

    Returns:
        Parent: The created parent entity.

    Raises:
        HTTPException: If creation fails.
    """
    return await controller.create(payload)


@router.delete(
    "/{user_id}/{student_id}",
    status_code=status.HTTP_200_OK,
    name="delete-parent",
    summary="Delete a parent",
    response_description="Returns the deleted parent info",
)
@inject
async def delete(
    user_id: int,
    student_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: ParentController = Depends(Provide[Container.parent_controller]),
):
    """
    Delete a parent-student association.

    Args:
        user_id (int): The parent's user ID.
        student_id (int): The student's ID.
        current_user (JwtPayload): The authenticated user.
        controller (ParentController): Controller to handle business logic.

    Returns:
        bool: True if deletion succeeded.

    Raises:
        HTTPException: If parent association not found or deletion fails.
    """
    return await controller.delete(user_id=user_id, student_id=student_id)
