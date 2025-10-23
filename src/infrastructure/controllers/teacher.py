from fastapi import HTTPException
import sentry_sdk
from src.application.use_case.teacher.create_teacher_case import CreateTeacherCase
from src.application.use_case.teacher.delete_teacher_case import DeleteTeacherCase
from src.application.use_case.teacher.find_teacher_case import FindTeacherCase
from src.infrastructure.exceptions.except_manager import manage_teacher_except


class TeacherController:
    def __init__(
        self,
        find_case: FindTeacherCase,
        create_case: CreateTeacherCase,
        delete_case: DeleteTeacherCase,
    ):
        self.find_case = find_case
        self.create_case = create_case
        self.delete_case = delete_case


    async def create(self, user_id: int):
        try:
            resp = await self.create_case.create(user_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deleted_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_teacher_except(e)


    async def delete(self, teacher_id: int):
        try:
            resp = await self.delete_case.delete(teacher_id=teacher_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deleted_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_teacher_except(e)


    async def get(self, teacher_id: int):
        try:
            teacher = await self.find_case.get_teacher_full_info(teacher_id=teacher_id)
            return {
                "status": "success",
                "data": teacher,
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_teacher_except(e)

    async def get_all(self):
        try:
            resp = await self.find_case.get_all()
            return {
                "status": "success",
                "data": resp,
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_teacher_except(e)
