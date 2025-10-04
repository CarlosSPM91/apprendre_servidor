
from typing import List

from fastapi import HTTPException, status
from src.domain.objects.role.role_dto import RoleDTO
from src.infrastructure.repositories.role import RoleRepository


class FindRoleCase:
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    async def get_all(
        self,
    ) -> List[RoleDTO]:
        
        role = await self.role_repo.get_roles()
        return role
    
    async def find_by_id(
        self,
        role_id: int
    ) -> RoleDTO:
        role = await self.role_repo.find_role(role_id)
        if role:
            return role
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= {
                    "status": "error",
                    "message": "Role not found"
                }
        )
    
    async def find_by_name(
        self,
        role_name: str
    ) -> RoleDTO:
        role = await self.role_repo.find_role_by_name(role_name)
        if role:
            return role
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= {
                    "status": "error",
                    "message": "Role not found"
                }
        )
