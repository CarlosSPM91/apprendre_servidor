"""
Users Endpoint.

Defines the API routes for user operations such as creation, retrieval, 
updating, password change, and deletion.

:author: Carlos S. Paredes Morillo
"""

from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.domain.objects.auth.change_pass_dto import ChangePasswordDTO
from src.domain.objects.token.jwtPayload import JwtPayload
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.controllers.user import UserController
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    name="me",
    summary="Get current authenticated user",
    response_description="Returns the current user's information",
)
@inject
async def me(
    controller: UserController = Depends(Provide[Container.user_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """Retrieve information about the currently authenticated user.

    Args:
        controller (UserController): The user controller injected by DI.
        current_user (JwtPayload): The current authenticated user's JWT payload.

    Returns:
        dict: The current user's data.
    """
    return await controller.me(current_user.user_id)

@router.get(
    "/sessions",
    status_code=status.HTTP_200_OK,
    name="me",
    summary="Get current authenticated user",
    response_description="Returns the current user's information",
)
@inject
async def me(
    controller: UserController = Depends(Provide[Container.user_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """Retrieve information about the total day sessions.

    Args:
        controller (UserController): The user controller injected by DI.
        current_user (JwtPayload): The current authenticated user's JWT payload.

    Returns:
        dict: The current user's data.
    """
    return await controller.get_sessions()

@router.get(
    "/access-logs",
    status_code=status.HTTP_200_OK,
    name="accces logs",
    summary="Get all the acces logs",
    response_description="Returns the information of acces logs",
)
@inject
async def get_access_logs(
    controller: UserController = Depends(Provide[Container.user_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """Retrieve information about logs of the users.

    Args:
        controller (UserController): The user controller injected by DI.
        current_user (JwtPayload): The current authenticated user's JWT payload.

    Returns:
        dict: The current user's data.
    """
    return await controller.get_access_logs()

@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="findAll",
    summary="Get all users",
    response_description="Returns a list of all users",
)
@inject
async def find_all_user(
    current_user: JwtPayload = Depends(get_current_user),
    controller: UserController = Depends(Provide[Container.user_controller]),
):
    """Retrieve all users in the system.

    Args:
        current_user (JwtPayload): Current authenticated user.
        controller (UserController): Controller handling user operations.

    Returns:
        list: List of UserDTO objects.
    """
    return await controller.get_all()

@router.get(
    "/{role_id}/all",
    status_code=status.HTTP_200_OK,
    name="find-all-by-role",
    summary="Get all users of one role",
    response_description="Returns a list of all users of one role",
)
@inject
async def find_all_user_by_role(
    role_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: UserController = Depends(Provide[Container.user_controller]),
):
    """Retrieve all users in the system.

    Args:
        current_user (JwtPayload): Current authenticated user.
        controller (UserController): Controller handling user operations.

    Returns:
        list: List of UserDTO objects.
    """
    return await controller.get_all_by_role(role_id=role_id)


@router.get(
    "/{user_id}/find",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get user by ID",
    response_description="Returns the user information by user ID",
)
@inject
async def find_user(
    user_id: int,
    controller: UserController = Depends(Provide[Container.user_controller]),
):
    """Retrieve a single user by their ID.

    Args:
        user_id (int): ID of the user to retrieve.
        controller (UserController): Controller handling user operations.

    Returns:
        dict: User information.
    """
    return await controller.get_user(user_id)


@router.post(
    "/create-user",
    status_code=status.HTTP_201_CREATED,
    name="create-user",
    summary="Create a new user",
    response_description="Returns the created user information",
)
@inject
async def create_user(
    payload: UserCreateDTO,
    controller: UserController = Depends(Provide[Container.user_controller]),
):
    """Create a new user in the system.

    Args:
        payload (UserCreateDTO): User creation payload.
        controller (UserController): Controller handling user operations.

    Returns:
        dict: Created user ID and timestamp.
    """
    return await controller.create_user(payload)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-user",
    summary="Update an existing user",
    response_description="Returns the updated user information",
)
@inject
async def update_user(
    payload: UserUpdateDTO,
    controller: UserController = Depends(Provide[Container.user_controller]),
):
    """Update an existing user's information.

    Args:
        payload (UserUpdateDTO): User update payload.
        controller (UserController): Controller handling user operations.

    Returns:
        dict: Updated user ID and timestamp.
    """
    return await controller.update_user(payload)


@router.put(
    "/change-password",
    status_code=status.HTTP_200_OK,
    name="change-password",
    summary="Change user's password",
    response_description="Returns the user ID and timestamp after password change",
)
@inject
async def change_password(
    payload: ChangePasswordDTO,
    controller: UserController = Depends(Provide[Container.user_controller]),
):
    """Change the password of a user.

    Args:
        payload (ChangePasswordDTO): Password change payload.
        controller (UserController): Controller handling user operations.

    Returns:
        dict: User ID and timestamp of password update.
    """
    return await controller.change_password(payload)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    name="delete-user",
    summary="Delete a user",
    response_description="Returns the deleted user ID and timestamp",
)
@inject
async def delete_user(
    user_id: int,
    controller: UserController = Depends(Provide[Container.user_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    """Delete a user from the system.

    Args:
        user_id (int): ID of the user to delete.
        controller (UserController): Controller handling user operations.
        current_user (JwtPayload): The authenticated user performing the deletion.

    Returns:
        dict: Deleted user ID and deletion timestamp.
    """
    return await controller.delete_user(user_id, current_user.user_id)
