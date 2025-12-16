from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.student_class import StudentClassController
from src.infrastructure.entities.course.student_class import StudentClass
from src.middleware.token.authenticateToken import get_current_user

router = APIRouter(prefix="/student_classes", tags=["student_classes"])


@router.get(
    "/{student_class_id}/all",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of all student classes",
    response_description="Returns a list of all student classes",
)
@inject
async def find_all(
    student_class_id: int,
    controller: StudentClassController = Depends(Provide[Container.student_class_controller]),
):
    """Retrieve all student classes in the system.

    Args:
        controller (StudentClassController): Controller handling student class operations.

    Returns:
        list: List of StudentClass objects.
    """
    return await controller.get_all(student_class_id)


@router.get(
    "/{student_class_id}",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of a student class",
    response_description="Returns the information of a student class",
)
@inject
async def find(
    student_class_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentClassController = Depends(Provide[Container.student_class_controller]),
):
    """Retrieve a single student class by its ID.

    Args:
        student_class_id (int): ID of the student class to retrieve.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (StudentClassController): Controller handling student class operations.

    Returns:
        dict: StudentClass information.
    """
    return await controller.get(student_class_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create a student class",
    response_description="Returns the information of a student class",
)
@inject
async def create(
    payload: StudentClass,
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentClassController = Depends(Provide[Container.student_class_controller]),
):
    """Create a new student class in the system.

    Args:
        payload (StudentClass): Payload containing student class data.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (StudentClassController): Controller handling student class operations.

    Returns:
        dict: Created student class ID and creation timestamp.
    """
    return await controller.create(payload)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-points",
    summary="Update points of a student class",
    response_description="Returns the updated student class",
)
@inject
async def update(
    payload: StudentClass,
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentClassController = Depends(Provide[Container.student_class_controller]),
):
    """Update points or other data of an existing student class.

    Args:
        payload (StudentClass): Payload containing updated student class data.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (StudentClassController): Controller handling student class operations.

    Returns:
        dict: Updated student class ID and timestamp.
    """
    return await controller.update_points(payload)


@router.delete(
    "/{student_class_id}",
    status_code=status.HTTP_200_OK,
    name="delete",
    summary="Delete a student class",
    response_description="Returns the deleted student class ID",
)
@inject
async def delete(
    student_class_id: int,
    controller: StudentClassController = Depends(Provide[Container.student_class_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """Delete a student class from the system by its ID.

    Args:
        student_class_id (int): ID of the student class to delete.
        controller (StudentClassController): Controller handling student class operations.
        current_user (JwtPayload): Authenticated user performing the deletion.

    Returns:
        dict: Deleted student class ID and deletion timestamp.
    """
    return await controller.delete(student_class_id)
