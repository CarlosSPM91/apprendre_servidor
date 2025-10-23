

from fastapi import HTTPException
import sentry_sdk
from src.application.use_case.parent.create_parent_case import CreateParentCase
from src.application.use_case.parent.delete_parent_case import DeleteParentCase
from src.application.use_case.parent.find_parent_case import FindParentCase
from src.infrastructure.entities.users.parents import Parent
from src.infrastructure.exceptions.except_manager import manage_parent_except


class ParentController:
    def __init__(
        self,
        find_case: FindParentCase,
        create_case: CreateParentCase,
        delete_case: DeleteParentCase,
    ):
        self.find_case = find_case
        self.create_case = create_case
        self.delete_case = delete_case

    async def create(self, payload: Parent):
        try:
            resp = await self.create_case.create(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deleted_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_parent_except(e)
    
    async def delete(self, user_id: int, student_id: int):
        try:
            resp = await self.delete_case.delete(user_id=user_id, student_id=student_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deleted_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_parent_except(e)

    async def get_parent(self, user_id: int):
        try:
            parent = await self.find_case.get(user_id=user_id)
            return {
                "status": "success",
                "data": parent,
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_parent_except(e)
    
    async def get_all(self):
        try:
            parents = await self.find_case.get_all()
            return {
                "status": "success",
                "data": parents,
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_parent_except(e)