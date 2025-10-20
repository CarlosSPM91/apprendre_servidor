
from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.allergy_info import AllergyController
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/allergy-info", tags=["allergy-info"])

@router.get(
    "/{allergy_id}/find",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of the allergy info",
    response_description="Returns the information of the allergy info",
)
@inject
async def find(
    allergy_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: AllergyController = Depends(Provide[Container.allergy_controller]),
):
    return await controller.get_allergy(allergy_id=allergy_id)

@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create the medical info",
    response_description="Returns the information of medical",
)
@inject
async def create(
    payload: AllergyInfo,
    current_user: JwtPayload = Depends(get_current_user),
    controller: AllergyController = Depends(Provide[Container.allergy_controller]),
):
    return await controller.create(payload)

@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-allergy",
    summary="Update an existing allergy info",
    response_description="Returns the updated allergy information",
)
@inject
async def update(
    payload: AllergyInfo,
    current_user: JwtPayload = Depends(get_current_user),
    controller: AllergyController = Depends(Provide[Container.allergy_controller]),
):
    print("-------- REPOSITORY update allergy -------- " + payload.description )
    return await controller.update(payload)

@router.delete(
    "/{allergy_id}",
    status_code=status.HTTP_200_OK,
    name="delete-allergy-info",
    summary="Delete a allergy info record",
    response_description="Returns the deleted allergy info ID and timestamp",
)
@inject
async def delete(
    allergy_id: int,
    controller: AllergyController = Depends(Provide[Container.allergy_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    return await controller.delete(allergy_id=allergy_id)