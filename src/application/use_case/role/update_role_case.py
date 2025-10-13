"""
Update Role Use Case.

Handles updating role information in the system.

:author: Carlos S. Paredes Morillo
"""

from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.role.role_dto import RoleDTO
from src.infrastructure.repositories.role import RoleRepository


class UpdateRoleCase:
    """Use case for updating role information."""

    def __init__(self, role_repo: RoleRepository):
        """
        Initialize the UpdateRoleCase with the required role repository.

        Args:
            role_repo (RoleRepository): Repository for managing role persistence.
        """
        self.role_repo = role_repo

    async def update(self, role_update: RoleDTO) -> CommonResponse:
        """
        Update a role's information.

        Args:
            role_update (RoleDTO): Data transfer object containing updated role info.

        Returns:
            CommonResponse: Contains the updated role's ID and the timestamp of the update.
        """
        role = await self.role_repo.update_role(role_update)
        return CommonResponse(
            item_id=role.role_id,
            event_date=datetime.now(timezone.utc)
        )

