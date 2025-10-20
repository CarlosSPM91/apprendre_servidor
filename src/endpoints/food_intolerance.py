
from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.food_intolrance import FoodIntoleranceController
from src.infrastructure.controllers.student import StudentController
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance
from src.middleware.token.authenticateToken import get_current_user, require_role


router = APIRouter(prefix="/food-intolerance", tags=["food-intolerance"])

@router.get(
    "/{intolerance_id}/find",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of the intolerance",
    response_description="Returns the information of the intolerance",
)
@inject
async def find(
    intolerance_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: FoodIntoleranceController = Depends(Provide[Container.food_intolerance_controller]),
):
    return await controller.get_intolerance(intolerance_id)

@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create the food intolerance",
    response_description="Returns the information of intolerance",
)
@inject
async def create(
    payload: FoodIntolerance,
    role:JwtPayload = Depends(require_role[1]),
    controller: FoodIntoleranceController = Depends(Provide[Container.food_intolerance_controller]),
):
    return await controller.create(payload)

@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-student",
    summary="Update an existing intolerance",
    response_description="Returns the updated intolerance information",
)
@inject
async def update(
    payload: FoodIntolerance,
    role:JwtPayload = Depends(require_role[1]),
    controller: FoodIntoleranceController = Depends(Provide[Container.food_intolerance_controller]),
):
    return await controller.update(payload)

@router.delete(
    "/{intolerance_id}",
    status_code=status.HTTP_200_OK,
    name="delete-intolerance",
    summary="Delete a intolerance",
    response_description="Returns the deleted intolerance ID and timestamp",
)
@inject
async def delete(
    intolerance_id: int,
    controller: FoodIntoleranceController = Depends(Provide[Container.food_intolerance_controller]),
    role:JwtPayload = Depends(require_role[1]),
):
    return await controller.delete(intolerance_id)