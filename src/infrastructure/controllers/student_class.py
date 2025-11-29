from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.student_class.create_student_class_case import CreateStudentClassCase
from src.application.use_case.student_class.delete_student_class_case import DeleteStudentClassCase
from src.application.use_case.student_class.find_student_class_case import FindStudentClassCase
from src.application.use_case.student_class.update_student_class_case import UpdateStudentClassCase
from src.infrastructure.entities.course.student_class import StudentClass
from src.infrastructure.exceptions.except_manager import manage_student_class_except

class StudentClassController:
    def __init__(
        self,
        find_case: FindStudentClassCase,
        create_case: CreateStudentClassCase,
        update_case: UpdateStudentClassCase,
        delete_case: DeleteStudentClassCase,
    ):
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, payload: StudentClass):
        try:
            resp = await self.create_case.create(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "created_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_class_except(e)

    async def update_points(self, payload: StudentClass):
        try:
            await self.find_case.get(payload.id)
            resp = await self.update_case.update(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "updated_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_class_except(e)

    async def delete(self, student_class_id: int):

        try:
            await self.find_case.get(student_class_id)
            resp = await self.delete_case.delete(
                student_class_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_class_except(e)

    async def get(self, student_class_id: str):
        try:
            resp = await self.find_case.get(student_class_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_class_except(e)
    
    async def get_all(self):
        try:
            resp = await self.find_case.get_all()
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_class_except(e)
