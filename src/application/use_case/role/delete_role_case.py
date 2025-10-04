from datetime import datetime, timezone

from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.role import RoleRepository


class DeleteRoleCase:
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    async def delete(
        self,
        role_id: int,
    ) -> CommonResponse:
        
        await self.role_repo.delete(role_id)
        return CommonResponse(
            item_id=role_id,
            event_date=datetime.now(timezone.utc)
        )
