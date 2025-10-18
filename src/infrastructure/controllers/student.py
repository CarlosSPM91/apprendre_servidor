from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.student.create_student_case import CreateStudenCase
from src.application.use_case.student.delete_student_case import DeleteStudentCase
from src.application.use_case.student.find_student_case import FindStudentCase
from src.application.use_case.student.update_student_case import UpdateStudentCase
from src.domain.exceptions.except_manager import manage_student_except
from src.infrastructure.entities.student_info.student import Student

class StudentController:
    def __init__(
        self,
        find_case: FindStudentCase,
        create_case: CreateStudenCase,
        update_case: UpdateStudentCase,
        delete_case: DeleteStudentCase,
    ):
        self.find_student_case = find_case
        self.create_student_case = create_case
        self.update_student_case = update_case
        self.delete_student_case = delete_case

    async def create(self, user_id: int):
        try:
            resp = await self.create_student_case.create(user_id=user_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "created_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_except(e)

    async def update(self, payload: Student):
        try:
            await self.find_student_case.get_student_by_id(payload.id)
            resp = await self.update_student_case.update_student(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "updated_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_except(e)

    async def delete(self, student_id: int):

        try:
            await self.find_student_case.get_student_by_id(student_id=student_id)
            resp = await self.delete_student_case.delete(
                student_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_except(e)

    async def get_student(self, student_id: str):
        try:
            return await self.find_student_case.get_student_by_id(student_id=student_id)
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_except(e)

    async def get_student_full_info(self, student_id: str):
        try:
            return await self.find_student_case.get_student_full_info(student_id=student_id)
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_except(e)