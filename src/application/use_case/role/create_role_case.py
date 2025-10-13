"""
Create Role Use Case.

Handles the creation of new roles in the system.

:author: Carlos S. Paredes Morillo
"""

from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.role import RoleRepository


class CreateRoleCase:
    """Use case for creating a new role."""

    def __init__(self, role_repo: RoleRepository):
        """
        Initialize the CreateRoleCase with the required role repository.

        Args:
            role_repo (RoleRepository): Repository for managing role persistence.
        """
        self.role_repo = role_repo

    async def create(self, role_name: str) -> CommonResponse:
        """
        Create a new role.

        Args:
            role_name (str): Name of the role to create.

        Returns:
            CommonResponse: Contains the new role's ID and the creation timestamp.
        """
        role = await self.role_repo.create(role_name)
        return CommonResponse(
            item_id=role.role_id,
            event_date=datetime.now(timezone.utc)
        )
