"""
Find Role Use Case.

Provides methods to retrieve roles by ID, name, or fetch all roles.

:author: Carlos S. Paredes Morillo
"""

from typing import List
from fastapi import HTTPException, status
from src.domain.objects.role.role_dto import RoleDTO
from src.infrastructure.repositories.role import RoleRepository


class FindRoleCase:
    """Use case for retrieving role information from the repository."""

    def __init__(self, role_repo: RoleRepository):
        """
        Initialize the FindRoleCase with the role repository.

        Args:
            role_repo (RoleRepository): Repository for accessing role data.
        """
        self.role_repo = role_repo

    async def get_all(self) -> List[RoleDTO]:
        """
        Retrieve all roles.

        Returns:
            List[RoleDTO]: List of all roles.
        """
        role = await self.role_repo.get_roles()
        return role

    async def find_by_id(self, role_id: int) -> RoleDTO:
        """
        Retrieve a role by its ID.

        Args:
            role_id (int): The ID of the role to retrieve.

        Returns:
            RoleDTO: Role data if found.

        Raises:
            HTTPException: If the role is not found (HTTP 404).
        """
        role = await self.role_repo.find_role(role_id)
        if role:
            return role
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": "Role not found"
            }
        )

    async def find_by_name(self, role_name: str) -> RoleDTO:
        """
        Retrieve a role by its name.

        Args:
            role_name (str): The name of the role to retrieve.

        Returns:
            RoleDTO: Role data if found.

        Raises:
            HTTPException: If the role is not found (HTTP 404).
        """
        role = await self.role_repo.find_role_by_name(role_name)
        if role:
            return role
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": "Role not found"
            }
        )
