"""
Users Controller.

Provides the controller layer between FastAPI endpoints and the application
services for user-related operations.

:author: Carlos S. Paredes Morillo
"""

from typing import List
from fastapi import HTTPException
import sentry_sdk
from src.application.use_case.user.create_user_case import CreateUserCase
from src.application.use_case.user.delete_user_case import DeleteUserCase
from src.application.use_case.user.find_user_case import FindUserCase
from src.application.use_case.user.update_user_case import UpdateUserCase
from src.domain.objects.auth.change_pass_dto import ChangePasswordDTO
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_dto import UserDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.exceptions.except_manager import manage_user_except


class UserController:
    """Controller for user operations.

    Acts as a bridge between the API layer and the application services.
    Handles creation, retrieval, update, deletion, and password management.
    """

    def __init__(
        self,
        find_case: FindUserCase,
        create_case: CreateUserCase,
        update_case: UpdateUserCase,
        delete_case: DeleteUserCase,
    ):
        """
        Initialize the UserController with the required use cases.

        Args:
            find_case (FindUserCase): Use case for retrieving users.
            create_case (CreateUserCase): Use case for creating users.
            update_case (UpdateUserCase): Use case for updating users.
            delete_case (DeleteUserCase): Use case for deleting users.
        """
        self.find_user_case = find_case
        self.create_user_case = create_case
        self.update_user_case = update_case
        self.delete_user_case = delete_case

    async def create_user(self, payload: UserCreateDTO):
        """
        Create a new user.

        Args:
            payload (UserCreateDTO): User creation data.

        Returns:
            dict: Status and created user information.

        Raises:
            HTTPException: If creation fails.
        """
        try:
            resp = await self.create_user_case.create(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "created_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def update_user(self, payload: UserUpdateDTO):
        """
        Update an existing user's information.

        Args:
            payload (UserUpdateDTO): User update data.

        Returns:
            dict: Status and updated user information.

        Raises:
            HTTPException: If update fails or user not found.
        """
        try:
            await self.find_user_case.get_user_by_id(payload.user_id)
            resp = await self.update_user_case.update_user(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "updated_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def change_password(self, payload: ChangePasswordDTO):
        """
        Change a user's password.

        Args:
            payload (ChangePasswordDTO): Password change data.

        Returns:
            dict: Status and information about the password change.

        Raises:
            HTTPException: If user not found or password change fails.
        """
        try:
            await self.find_user_case.get_user_by_id(payload.user_id)
            resp = await self.update_user_case.change_password(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "update_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def get_all(self):
        """
        Retrieve all users.

        Returns:
            dict: Status and list of users.

        Raises:
            HTTPException: If retrieval fails or no users found.
        """
        try:
            resp: List[UserDTO] = await self.find_user_case.get_all()
            return {
                "status": "success",
                "data": resp,
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def get_all_by_role(self, role_id: int):
        """
        Retrieve all users of a determinate role.

        Returns:
            dict: Status and list of users by role.

        Raises:
            HTTPException: If retrieval fails or no users found.
        """
        try:
            resp: List[UserDTO] = await self.find_user_case.get_all_by_role(
                role_id=role_id
            )
            return {
                "status": "success",
                "data": resp,
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def get_user(self, user_id: str):
        """
        Retrieve a single user by ID.

        Args:
            user_id (str): User identifier.

        Returns:
            UserDTO: User information.

        Raises:
            HTTPException: If user not found.
        """
        try:
            return await self.find_user_case.get_user_by_id(user_id)
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def get_sessions(self):
        """
        Retrieve a total user sessions.

        Returns:
            int: number of sessions.
        """
        try:
            resp = await self.find_user_case.get_day_sessions()
            return {
                "status": "success",
                "data": {"total_sessions": resp},
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def me(self, user_id: str):
        """
        Retrieve information about the current authenticated user.

        Args:
            user_id (str): User identifier.

        Returns:
            UserDTO: Current user information.

        Raises:
            HTTPException: If user not found.
        """
        try:
            return await self.find_user_case.get_user_by_id(user_id)
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)

    async def delete_user(self, user_id: int, user_eraser_id: int):
        """
        Delete a user and log who performed the deletion.

        Args:
            user_id (int): ID of the user to delete.
            user_eraser_id (int): ID of the user performing the deletion.

        Returns:
            dict: Status and deletion information.

        Raises:
            HTTPException: If deletion fails or user not found.
        """
        try:
            await self.find_user_case.get_user_by_id(user_id)
            resp = await self.delete_user_case.delete(
                user_id, user_who_delete=user_eraser_id
            )
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_user_except(e)
