
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
    name="find",
    summary="Get information of all allergy info",
    response_description="Returns a list of all the allergy info",
)
@inject
async def find_all(
    controller: MedicalInfoController = Depends(Provide[Container.medical_info_controller]),
):
    return await controller.get_all()

@router.get(
    "/{medical_id}/find",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of the medical info",
    response_description="Returns the information of the medical info",
)
@inject
async def find(
    medical_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: MedicalInfoController = Depends(Provide[Container.medical_info_controller]),
):
    return await controller.get_medical(medical_id=medical_id)

@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create the medical info",
    response_description="Returns the information of medical",
)
@inject
async def create(
    payload: MedicalInfo,
    current_user: JwtPayload = Depends(get_current_user),
    controller: MedicalInfoController = Depends(Provide[Container.medical_info_controller]),
):
    return await controller.create(payload)

@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-medical-info",
    summary="Update an existing medical info",
    response_description="Returns the updated medical information",
)
@inject
async def update(
    payload: MedicalInfo,
    current_user: JwtPayload = Depends(get_current_user),
    controller: MedicalInfoController = Depends(Provide[Container.medical_info_controller]),
):
    return await controller.update(payload)

@router.delete(
    "/{medical_id}",
    status_code=status.HTTP_200_OK,
    name="delete-medical-info",
    summary="Delete a medical info record",
    response_description="Returns the deleted medical info ID and timestamp",
)
@inject
async def delete(
    medical_id: int,
    controller: MedicalInfoController = Depends(Provide[Container.medical_info_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    return await controller.delete(medical_id=medical_id)