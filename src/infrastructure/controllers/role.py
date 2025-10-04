from fastapi import HTTPException

from src.application.use_case.role.create_role_case import CreateRoleCase
from src.application.use_case.role.delete_role_case import DeleteRoleCase
from src.application.use_case.role.find_role_case import FindRoleCase
from src.application.use_case.role.update_role_case import UpdateRoleCase
from src.domain.exceptions.except_manager import manage_role_except
from src.domain.objects.role.role_dto import RoleDTO


class RoleController:
    def __init__(
        self,
        create_role_case: CreateRoleCase,
        find_role_case: FindRoleCase,
        update_role_case: UpdateRoleCase,
        delete_role_case: DeleteRoleCase,
    ):
        self.create_role_case = create_role_case
        self.find_role_case = find_role_case
        self.update_role_case = update_role_case
        self.delete_role_case = delete_role_case

    async def get_all(self):
        try:
            resp = await self.find_role_case.get_all()
            return {
                "status": "success",
                "data": resp,
            }
        except HTTPException as e:
            manage_role_except(e)

    async def create_role(self, role_name: str):
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
            manage_role_except(e)

    async def update_role(self, role: RoleDTO):
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
            manage_role_except(e)

    async def deleterole(self, role_id: int):
        try:
            await self.delete_role_case.delete(role_id)
            resp = await self.delete_role_case.delete(role_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            manage_role_except(e)
