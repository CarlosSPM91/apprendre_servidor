from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.subject_class import SubjectClassController
from src.infrastructure.entities.course.school_subject import SchoolSubject
from src.infrastructure.entities.course.subject_class import SubjectClass
from src.middleware.token.authenticateToken import get_current_user

router = APIRouter(prefix="/subject_classes", tags=["subject_classes"])


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of all subject classes",
    response_description="Returns a list of all subject classes",
)
@inject
async def find_all(
    controller: SubjectClassController = Depends(Provide[Container.subject_class_controller]),
):
    """Retrieve all subject classes in the system.

    Args:
        controller (SubjectClassController): Controller handling subject class operations.

    Returns:
        list: List of subject class objects.
    """
    return await controller.get_all()


@router.get(
    "/{subject_class_id}",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of a subject class",
    response_description="Returns the information of a subject class",
)
@inject
async def find(
    subject_class_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: SubjectClassController = Depends(Provide[Container.subject_class_controller]),
):
    """Retrieve a single subject class by its ID.

    Args:
        subject_class_id (int): ID of the subject class to retrieve.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (SubjectClassController): Controller handling subject class operations.

    Returns:
        dict: Subject class information.
    """
    return await controller.get(subject_class_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create a subject class",
    response_description="Returns the information of the created subject class",
)
@inject
async def create(
    payload: SubjectClass,
    current_user: JwtPayload = Depends(get_current_user),
    controller: SubjectClassController = Depends(Provide[Container.subject_class_controller]),
):
    """Create a new subject class in the system.

    Args:
        payload (SubjectClass): Payload containing subject class data.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (SubjectClassController): Controller handling subject class operations.

    Returns:
        dict: Created subject class ID and creation timestamp.
    """
    return await controller.create(payload)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update",
    summary="Update an existing subject class",
    response_description="Returns the updated subject class",
)
@inject
async def update(
    payload: SubjectClass,
    current_user: JwtPayload = Depends(get_current_user),
    controller: SubjectClassController = Depends(Provide[Container.subject_class_controller]),
):
    """Update an existing subject class.

    Args:
        payload (SubjectClass): Payload containing updated subject class data.
        current_user (JwtPayload): Authenticated user's JWT payload.
        controller (SubjectClassController): Controller handling subject class operations.

    Returns:
        dict: Updated subject class ID and timestamp.
    """
    return await controller.update(payload)


@router.delete(
    "/{subject_class_id}",
    status_code=status.HTTP_200_OK,
    name="delete",
    summary="Delete a subject class",
    response_description="Returns the deleted subject class ID",
)
@inject
async def delete(
    subject_class_id: int,
    controller: SubjectClassController = Depends(Provide[Container.subject_class_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """Delete a subject class from the system by its ID.

    Args:
        subject_class_id (int): ID of the subject class to delete.
        controller (SubjectClassController): Controller handling subject class operations.
        current_user (JwtPayload): Authenticated user performing the deletion.

    Returns:
        dict: Deleted subject class ID and deletion timestamp.
    """
    return await controller.delete(subject_class_id)
