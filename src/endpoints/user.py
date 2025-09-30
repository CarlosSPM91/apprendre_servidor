"""
Users Endpoint.

Defines the API routes for user operations (creation, retrieval, etc.).

:author: Carlos S. Paredes Morillo
"""
from fastapi import APIRouter, Depends, status

from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.infrastructure.controllers.user import UserController


router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.post(
    "/create-user",
    status_code=status.HTTP_201_CREATED,
    name="create-user"
)
async def create_user(
    payload: UserCreateDTO,
    controller: UserController = Depends()
):
    """Create a new user.

    Args:
        payload (UserCreateDTO): Data required to create a user.
        controller (UserController): User controller instance injected by FastAPI.

    Returns:
        dict: Response with the created user details.

    :author: Carlos S. Paredes Morillo
    """
    return await controller.create_user(payload)