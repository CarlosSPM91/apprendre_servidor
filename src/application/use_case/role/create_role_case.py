from datetime import datetime, timezone

from fastapi import HTTPException, status
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.role.role_dto import RoleDTO
from src.infrastructure.repositories.role import RoleRepository


class CreateRoleCase:
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    async def create(
        self,
        role_name: str,
    ) -> CommonResponse:
        
        role = await self.role_repo.create(role_name)
        return CommonResponse(
            item_id=role.role_id,
            event_date=datetime.now(timezone.utc)
        )
