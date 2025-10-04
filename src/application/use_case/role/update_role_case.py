from datetime import datetime, timezone

from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.role.role_dto import RoleDTO
from src.infrastructure.repositories.role import RoleRepository


class UpdateRoleCase:
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    async def update(
        self,
        role_update: RoleDTO,
    ) -> CommonResponse:
        
        role = await self.role_repo.update_role(role_update)
        return CommonResponse(
            item_id=role.role_id,
            event_date=datetime.now(timezone.utc)
        )
