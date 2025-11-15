
from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.profiles.student_update_dto import StudentUpdateDTO
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.student import StudentController
from src.infrastructure.entities.student_info.student import Student
from src.middleware.token.authenticateToken import get_current_user

"""
Students Endpoints.

Provides API routes for managing Student entities.

:author: Carlos S. Paredes Morillo
"""


router = APIRouter(prefix="/students", tags=["students"])
@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find-all-students",
    summary="Get all students",
    response_description="Returns a list of all students",
)
@inject
async def find(
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentController = Depends(Provide[Container.student_contoller]),
):
    """
    Retrieve all students.

    Args:
        current_user (JwtPayload): The authenticated user.
        controller (StudentController): Controller to handle business logic.

    Returns:
        List[Student]: List of all students.

    Raises:
        HTTPException: If no students found or an error occurs.
    """
    return await controller.get_all()


@router.get(
    "/{student_id}/find",
    status_code=status.HTTP_200_OK,
    name="find-student",
    summary="Get information of a student",
    response_description="Returns the information of student",
)
@inject
async def find(
    student_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentController = Depends(Provide[Container.student_contoller]),
):
    """
    Retrieve full information of a specific student.

    Args:
        student_id (int): The student's ID.
        current_user (JwtPayload): The authenticated user.
        controller (StudentController): Controller to handle business logic.

    Returns:
        StudentInfoDTO: Full student information including medical, allergy, and intolerance data.

    Raises:
        HTTPException: If student not found or retrieval fails.
    """
    return await controller.get_student_full_info(student_id=student_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create-student",
    summary="Create a student",
    response_description="Returns the created student",
)
@inject
async def create(
    user_id:int = Body(..., embed=True),
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentController = Depends(Provide[Container.student_contoller]),
):
    """
    Create a new student.

    Args:
        user_id (int): ID of the user to become a student.
        current_user (JwtPayload): The authenticated user.
        controller (StudentController): Controller to handle business logic.

    Returns:
        Student: The newly created student.

    Raises:
        HTTPException: If student already exists or creation fails.
    """
    return await controller.create(user_id=user_id)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-student",
    summary="Update an existing student",
    response_description="Returns the updated student information",
)
@inject
async def update_user(
    payload: StudentUpdateDTO,
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentController = Depends(Provide[Container.student_contoller]),
):
    """
    Update an existing student's information.

    Args:
        payload (StudentUpdateDTO): Data for updating the student.
        current_user (JwtPayload): The authenticated user.
        controller (StudentController): Controller to handle business logic.

    Returns:
        Student: The updated student entity.

    Raises:
        HTTPException: If student not found or update fails.
    """
    return await controller.update(payload)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    name="delete-student",
    summary="Delete a student",
    response_description="Returns the deleted student ID",
)
@inject
async def delete_student(
    student_id: int,
    controller: StudentController = Depends(Provide[Container.student_contoller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """
    Delete a student by ID.

    Args:
        student_id (int): ID of the student to delete.
        current_user (JwtPayload): The authenticated user.
        controller (StudentController): Controller to handle business logic.

    Returns:
        bool: True if deletion succeeded.

    Raises:
        HTTPException: If student not found or deletion fails.
    """
    return await controller.delete(student_id=student_id)
