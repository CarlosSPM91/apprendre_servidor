"""
Role Controller.

Handles CRUD operations for Role entities.
Integrates with use cases for create, update, delete, and fetch operations,
and captures exceptions using Sentry.

:author: Carlos S. Paredes Morillo
"""

from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.role.create_role_case import CreateRoleCase
from src.application.use_case.role.delete_role_case import DeleteRoleCase
from src.application.use_case.role.find_role_case import FindRoleCase
from src.application.use_case.role.update_role_case import UpdateRoleCase
from src.domain.objects.role.role_dto import RoleDTO
from src.infrastructure.exceptions.except_manager import manage_role_except


class RoleController:
    """Controller for Role-related endpoints."""

    def __init__(
        self,
        create_role_case: CreateRoleCase,
        find_role_case: FindRoleCase,
        update_role_case: UpdateRoleCase,
        delete_role_case: DeleteRoleCase,
    ):
        """
        Initialize RoleController with the required use cases.

        Args:
            create_role_case (CreateRoleCase): Use case for creating roles.
            find_role_case (FindRoleCase): Use case for retrieving roles.
            update_role_case (UpdateRoleCase): Use case for updating roles.
            delete_role_case (DeleteRoleCase): Use case for deleting roles.
        """
        self.create_role_case = create_role_case
        self.find_role_case = find_role_case
        self.update_role_case = update_role_case
        self.delete_role_case = delete_role_case

    async def get_all(self):
        """
        Retrieve all roles.

        Returns:
            dict: Contains status and list of RoleDTOs.

        Raises:
            HTTPException: If fetching roles fails.
        """
        try:
            resp = await self.find_role_case.get_all()
            return {
                "status": "success",
                "data": resp,
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_role_except(e)

    async def create_role(self, role_name: str):
        """
        Create a new role.

        Args:
            role_name (str): Name of the role to create.

        Returns:
            dict: Status and information about created role.

        Raises:
            HTTPException: If creation fails.
        """
        try:
            resp = await self.create_role_case.create(role_name)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "created_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_role_except(e)

    async def update_role(self, role: RoleDTO):
        """
        Update an existing role.

        Args:
            role (RoleDTO): Role data to update.

        Returns:
            dict: Status and update information.

        Raises:
            HTTPException: If update fails or role does not exist.
        """
        try:
            await self.find_role_case.find_by_id(role.role_id)
            resp = await self.update_role_case.update(role)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "update_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_role_except(e)

    async def deleterole(self, role_id: int):
        """
        Delete a role by its ID.

        Args:
            role_id (int): ID of the role to delete.

        Returns:
            dict: Status and deletion information.

        Raises:
            HTTPException: If deletion fails or role does not exist.
        """
        try:
            resp = await self.delete_role_case.delete(role_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_role_except(e)
