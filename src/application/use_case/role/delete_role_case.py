"""
Delete Role Use Case.

Handles the deletion of roles in the system.

:author: Carlos S. Paredes Morillo
"""

from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.role import RoleRepository


class DeleteRoleCase:
    """Use case for deleting a role."""

    def __init__(self, role_repo: RoleRepository):
        """
        Initialize the DeleteRoleCase with the required role repository.

        Args:
            role_repo (RoleRepository): Repository for managing role persistence.
        """
        self.role_repo = role_repo

    async def delete(self, role_id: int) -> CommonResponse:
        """
        Delete a role by its ID.

        Args:
            role_id (int): The ID of the role to delete.

        Returns:
            CommonResponse: Contains the deleted role's ID and the timestamp of the deletion.
        """
        await self.role_repo.delete(role_id)
        return CommonResponse(
            item_id=role_id,
            event_date=datetime.now(timezone.utc)
        )
