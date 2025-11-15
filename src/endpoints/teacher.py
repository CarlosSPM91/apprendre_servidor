from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.domain.objects.profiles.teacher_dto import TeacherDTO
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.teacher import TeacherController
from src.middleware.token.authenticateToken import get_current_user

"""
Teachers Endpoints.

Provides API routes for managing Teacher entities.

:author: Carlos S. Paredes Morillo
"""


router = APIRouter(prefix="/teachers", tags=["teachers"])

@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find-all-teacher",
    summary="Get all teachers",
    response_description="Returns a list of teachers",
)
@inject
async def find_all(
    current_user: JwtPayload = Depends(get_current_user),
    controller: TeacherController = Depends(Provide[Container.teacher_controller])
):
    """
    Retrieve all teachers.

    Args:
        current_user (JwtPayload): The authenticated user.
        controller (TeacherController): Controller to handle business logic.

    Returns:
        List[TeacherDTO]: A list of all teachers.

    Raises:
        HTTPException: If there is an error fetching teachers.
    """
    return await controller.get_all()


@router.get(
    "/{teacher_id}",
    status_code=status.HTTP_200_OK,
    name="findTeacher",
    summary="Get one teacher",
    response_description="Returns information of a teacher",
)
@inject
async def find(
    teacher_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: TeacherController = Depends(Provide[Container.teacher_controller])
):
    """
    Retrieve a specific teacher by ID.

    Args:
        teacher_id (int): The teacher's ID.
        current_user (JwtPayload): The authenticated user.
        controller (TeacherController): Controller to handle business logic.

    Returns:
        TeacherDTO: Information about the teacher.

    Raises:
        HTTPException: If teacher not found or an error occurs.
    """
    return await controller.get(teacher_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="createTeacher",
    summary="Create a teacher",
    response_description="Returns the created teacher",
)
@inject
async def create(
    user_id: int = Body(..., embed=True),
    current_user: JwtPayload = Depends(get_current_user),
    controller: TeacherController = Depends(Provide[Container.teacher_controller])
):
    """
    Create a new teacher linked to a user.

    Args:
        user_id (int): ID of the user to become a teacher.
        current_user (JwtPayload): The authenticated user.
        controller (TeacherController): Controller to handle business logic.

    Returns:
        TeacherDTO: The newly created teacher.

    Raises:
        HTTPException: If teacher already exists or creation fails.
    """
    return await controller.create(user_id)


@router.delete(
    "/{teacher_id}",
    status_code=status.HTTP_200_OK,
    name="deleteTeacher",
    summary="Delete one teacher",
    response_description="Delete one teacher"
)
@inject
async def delete(
    teacher_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: TeacherController = Depends(Provide[Container.teacher_controller])
):
    """
    Delete a teacher by ID.

    Args:
        teacher_id (int): ID of the teacher to delete.
        current_user (JwtPayload): The authenticated user.
        controller (TeacherController): Controller to handle business logic.

    Returns:
        bool: True if deletion succeeded.

    Raises:
        HTTPException: If teacher not found or deletion fails.
    """
    return await controller.delete(teacher_id)
