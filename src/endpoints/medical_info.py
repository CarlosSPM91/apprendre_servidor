
from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.medical_info import MedicalInfoController
from src.infrastructure.entities.student_info.medical_info import MedicalInfo
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/medical-info", tags=["medical-info"])

@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find-all-medical-info",
    summary="Get all medical info",
    response_description="Returns a list of all medical info records",
)
@inject
async def find_all(
    controller: MedicalInfoController = Depends(Provide[Container.medical_info_controller]),
):
    """
    Retrieve all medical info records.

    Args:
        controller (MedicalInfoController): Controller handling medical info logic.

    Returns:
        List[MedicalInfo]: List of all medical info records.

    Raises:
        HTTPException: If retrieval fails.
    """
    return await controller.get_all()


@router.get(
    "/{medical_id}/find",
    status_code=status.HTTP_200_OK,
    name="find-medical-info",
    summary="Get a specific medical info",
    response_description="Returns information of a specific medical info record",
)
@inject
async def find(
    medical_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: MedicalInfoController = Depends(Provide[Container.medical_info_controller]),
):
    """
    Retrieve a specific medical info record by ID.

    Args:
        medical_id (int): ID of the medical info record.
        current_user (JwtPayload): Authenticated user.
        controller (MedicalInfoController): Controller handling medical info logic.

    Returns:
        MedicalInfo: The requested medical info record.

    Raises:
        HTTPException: If record not found or retrieval fails.
    """
    return await controller.get_medical(medical_id=medical_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create-medical-info",
    summary="Create a medical info record",
    response_description="Returns the created medical info record",
)
@inject
async def create(
    payload: MedicalInfo,
    current_user: JwtPayload = Depends(get_current_user),
    controller: MedicalInfoController = Depends(Provide[Container.medical_info_controller]),
):
    """
    Create a new medical info record.

    Args:
        payload (MedicalInfo): The medical info data to create.
        current_user (JwtPayload): Authenticated user.
        controller (MedicalInfoController): Controller handling medical info logic.

    Returns:
        MedicalInfo: The newly created medical info record.

    Raises:
        HTTPException: If creation fails.
    """
    return await controller.create(payload)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-medical-info",
    summary="Update a medical info record",
    response_description="Returns the updated medical info record",
)
@inject
async def update(
    payload: MedicalInfo,
    current_user: JwtPayload = Depends(get_current_user),
    controller: MedicalInfoController = Depends(Provide[Container.medical_info_controller]),
):
    """
    Update an existing medical info record.

    Args:
        payload (MedicalInfo): The updated medical info data.
        current_user (JwtPayload): Authenticated user.
        controller (MedicalInfoController): Controller handling medical info logic.

    Returns:
        MedicalInfo: The updated medical info record.

    Raises:
        HTTPException: If update fails or record not found.
    """
    return await controller.update(payload)


@router.delete(
    "/{medical_id}",
    status_code=status.HTTP_200_OK,
    name="delete-medical-info",
    summary="Delete a medical info record",
    response_description="Returns the deleted medical info ID",
)
@inject
async def delete(
    medical_id: int,
    controller: MedicalInfoController = Depends(Provide[Container.medical_info_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """
    Delete a medical info record by ID.

    Args:
        medical_id (int): ID of the medical info to delete.
        current_user (JwtPayload): Authenticated user.
        controller (MedicalInfoController): Controller handling medical info logic.

    Returns:
        bool: True if deletion succeeded.

    Raises:
        HTTPException: If record not found or deletion fails.
    """
    return await controller.delete(medical_id=medical_id)
