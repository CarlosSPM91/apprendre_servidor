from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.domain.objects.classes.update_class_subjects_dto import UpdateClassSubjectsDTO
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.classes import ClassesController
from src.infrastructure.entities.course.classes import Classes
from src.middleware.token.authenticateToken import get_current_user

router = APIRouter(prefix="/classes", tags=["class"])


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find_all",
    summary="Get information of all classes",
    response_description="Returns a list of all classes",
)
@inject
async def find_all(
    controller: ClassesController = Depends(Provide[Container.classes_controller]),
):
    """Retrieve all classes in the system.

    Args:
        controller (ClassesController): Controller handling class operations.

    Returns:
        list: List of all Classes objects.
    """
    return await controller.get_all()


@router.get(
    "/{classes_id}",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of a class",
    response_description="Returns the information of a class",
)
@inject
async def find(
    classes_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: ClassesController = Depends(Provide[Container.classes_controller]),
):
    """Retrieve a single class by its ID.

    Args:
        classes_id (int): ID of the class to retrieve.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (ClassesController): Controller handling class operations.

    Returns:
        dict: Class information.
    """
    return await controller.get(classes_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create a class",
    response_description="Returns the information of the created class",
)
@inject
async def create(
    payload: Classes,
    current_user: JwtPayload = Depends(get_current_user),
    controller: ClassesController = Depends(Provide[Container.classes_controller]),
):
    """Create a new class in the system.

    Args:
        payload (Classes): Payload containing class data to create.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (ClassesController): Controller handling class operations.

    Returns:
        dict: Created class ID and creation timestamp.
    """
    return await controller.create(payload)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-class",
    summary="Update an existing class",
    response_description="Returns the updated class",
)
@inject
async def update(
    payload: Classes,
    current_user: JwtPayload = Depends(get_current_user),
    controller: ClassesController = Depends(Provide[Container.classes_controller]),
):
    """Update information of an existing class.

    Args:
        payload (Classes): Payload containing updated class data.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (ClassesController): Controller handling class operations.

    Returns:
        dict: Updated class ID and timestamp.
    """
    return await controller.update(payload)


@router.put(
    "/subjects",
    status_code=status.HTTP_200_OK,
    name="update-class-subjects",
    summary="Update an existing class with subjects",
    response_description="Returns the updated subjects of a class",
)
@inject
async def update_subjects(
    payload: UpdateClassSubjectsDTO,
    current_user: JwtPayload = Depends(get_current_user),
    controller: ClassesController = Depends(Provide[Container.classes_controller]),
):
    """Update the subjects associated with a specific class.

    Args:
        payload (UpdateClassSubjectsDTO): DTO containing class ID and subject updates.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (ClassesController): Controller handling class operations.

    Returns:
        dict: Updated class ID and timestamp.
    """
    return await controller.update_subjects(payload)


@router.delete(
    "/{classes_id}",
    status_code=status.HTTP_200_OK,
    name="delete-class",
    summary="Delete a class",
    response_description="Returns the deleted class ID and timestamp",
)
@inject
async def delete(
    classes_id: int,
    controller: ClassesController = Depends(Provide[Container.classes_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """Delete a class from the system by its ID.

    Args:
        classes_id (int): ID of the class to delete.
        controller (ClassesController): Controller handling class operations.
        current_user (JwtPayload): Authenticated user's JWT payload.

    Returns:
        dict: Deleted class ID and deletion timestamp.
    """
    return await controller.delete(classes_id)
