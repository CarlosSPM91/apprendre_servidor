
from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.food_intolrance import FoodIntoleranceController
from src.infrastructure.controllers.student import StudentController
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/food-intolerance", tags=["food-intolerance"])
@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find-all-food-intolerance",
    summary="Get all food intolerances",
    response_description="Returns a list of all food intolerance records",
)
@inject
async def find_all(
    controller: FoodIntoleranceController = Depends(Provide[Container.food_intolerance_controller]),
):
    """
    Retrieve all food intolerance records.

    Args:
        controller (FoodIntoleranceController): Controller handling food intolerance logic.

    Returns:
        List[FoodIntolerance]: List of all food intolerance records.

    Raises:
        HTTPException: If retrieval fails.
    """
    return await controller.get_all()


@router.get(
    "/{intolerance_id}/find",
    status_code=status.HTTP_200_OK,
    name="find-food-intolerance",
    summary="Get a specific food intolerance",
    response_description="Returns information of a specific food intolerance record",
)
@inject
async def find(
    intolerance_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: FoodIntoleranceController = Depends(Provide[Container.food_intolerance_controller]),
):
    """
    Retrieve a specific food intolerance record by ID.

    Args:
        intolerance_id (int): ID of the food intolerance record.
        current_user (JwtPayload): Authenticated user.
        controller (FoodIntoleranceController): Controller handling food intolerance logic.

    Returns:
        FoodIntolerance: The requested food intolerance record.

    Raises:
        HTTPException: If record not found or retrieval fails.
    """
    return await controller.get_intolerance(intolerance_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create-food-intolerance",
    summary="Create a food intolerance record",
    response_description="Returns the created food intolerance record",
)
@inject
async def create(
    payload: FoodIntolerance,
    current_user: JwtPayload = Depends(get_current_user),
    controller: FoodIntoleranceController = Depends(Provide[Container.food_intolerance_controller]),
):
    """
    Create a new food intolerance record.

    Args:
        payload (FoodIntolerance): The food intolerance data to create.
        current_user (JwtPayload): Authenticated user.
        controller (FoodIntoleranceController): Controller handling food intolerance logic.

    Returns:
        FoodIntolerance: The newly created food intolerance record.

    Raises:
        HTTPException: If creation fails.
    """
    return await controller.create(payload)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-food-intolerance",
    summary="Update an existing food intolerance record",
    response_description="Returns the updated food intolerance record",
)
@inject
async def update(
    payload: FoodIntolerance,
    current_user: JwtPayload = Depends(get_current_user),
    controller: FoodIntoleranceController = Depends(Provide[Container.food_intolerance_controller]),
):
    """
    Update an existing food intolerance record.

    Args:
        payload (FoodIntolerance): The updated food intolerance data.
        current_user (JwtPayload): Authenticated user.
        controller (FoodIntoleranceController): Controller handling food intolerance logic.

    Returns:
        FoodIntolerance: The updated food intolerance record.

    Raises:
        HTTPException: If update fails or record not found.
    """
    return await controller.update(payload)


@router.delete(
    "/{intolerance_id}",
    status_code=status.HTTP_200_OK,
    name="delete-food-intolerance",
    summary="Delete a food intolerance record",
    response_description="Returns the deleted food intolerance ID",
)
@inject
async def delete(
    intolerance_id: int,
    controller: FoodIntoleranceController = Depends(Provide[Container.food_intolerance_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """
    Delete a food intolerance record by ID.

    Args:
        intolerance_id (int): ID of the food intolerance record to delete.
        current_user (JwtPayload): Authenticated user.
        controller (FoodIntoleranceController): Controller handling food intolerance logic.

    Returns:
        bool: True if deletion succeeded.

    Raises:
        HTTPException: If record not found or deletion fails.
    """
    return await controller.delete(intolerance_id)
