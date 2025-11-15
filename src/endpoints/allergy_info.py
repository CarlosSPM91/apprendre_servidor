
from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.allergy_info import AllergyController
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/allergy-info", tags=["allergy-info"])

@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find-all-allergy-info",
    summary="Get all allergy info",
    response_description="Returns a list of all allergy info records",
)
@inject
async def find_all(
    controller: AllergyController = Depends(Provide[Container.allergy_controller]),
):
    """
    Retrieve all allergy info records.

    Args:
        controller (AllergyController): Controller handling allergy info logic.

    Returns:
        List[AllergyInfo]: List of all allergy info records.

    Raises:
        HTTPException: If retrieval fails.
    """
    return await controller.get_all()


@router.get(
    "/{allergy_id}/find",
    status_code=status.HTTP_200_OK,
    name="find-allergy-info",
    summary="Get a specific allergy info",
    response_description="Returns information of a specific allergy info record",
)
@inject
async def find(
    allergy_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: AllergyController = Depends(Provide[Container.allergy_controller]),
):
    """
    Retrieve a specific allergy info record by ID.

    Args:
        allergy_id (int): ID of the allergy info record.
        current_user (JwtPayload): Authenticated user.
        controller (AllergyController): Controller handling allergy info logic.

    Returns:
        AllergyInfo: The requested allergy info record.

    Raises:
        HTTPException: If record not found or retrieval fails.
    """
    return await controller.get_allergy(allergy_id=allergy_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create-allergy-info",
    summary="Create an allergy info record",
    response_description="Returns the created allergy info record",
)
@inject
async def create(
    payload: AllergyInfo,
    current_user: JwtPayload = Depends(get_current_user),
    controller: AllergyController = Depends(Provide[Container.allergy_controller]),
):
    """
    Create a new allergy info record.

    Args:
        payload (AllergyInfo): The allergy info data to create.
        current_user (JwtPayload): Authenticated user.
        controller (AllergyController): Controller handling allergy info logic.

    Returns:
        AllergyInfo: The newly created allergy info record.

    Raises:
        HTTPException: If creation fails.
    """
    return await controller.create(payload)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-allergy-info",
    summary="Update an existing allergy info record",
    response_description="Returns the updated allergy info record",
)
@inject
async def update(
    payload: AllergyInfo,
    current_user: JwtPayload = Depends(get_current_user),
    controller: AllergyController = Depends(Provide[Container.allergy_controller]),
):
    """
    Update an existing allergy info record.

    Args:
        payload (AllergyInfo): The updated allergy info data.
        current_user (JwtPayload): Authenticated user.
        controller (AllergyController): Controller handling allergy info logic.

    Returns:
        AllergyInfo: The updated allergy info record.

    Raises:
        HTTPException: If update fails or record not found.
    """
    return await controller.update(payload)


@router.delete(
    "/{allergy_id}",
    status_code=status.HTTP_200_OK,
    name="delete-allergy-info",
    summary="Delete an allergy info record",
    response_description="Returns the deleted allergy info ID",
)
@inject
async def delete(
    allergy_id: int,
    controller: AllergyController = Depends(Provide[Container.allergy_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """
    Delete an allergy info record by ID.

    Args:
        allergy_id (int): ID of the allergy info to delete.
        current_user (JwtPayload): Authenticated user.
        controller (AllergyController): Controller handling allergy info logic.

    Returns:
        bool: True if deletion succeeded.

    Raises:
        HTTPException: If record not found or deletion fails.
    """
    return await controller.delete(allergy_id=allergy_id)
