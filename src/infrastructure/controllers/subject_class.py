from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.subject_class.create_subject_class_case import CreateSubjectClassCase
from src.application.use_case.subject_class.delete_subject_class_case import DeleteSubjectClassCase
from src.application.use_case.subject_class.find_subject_class_case import FindSubjectClassCase
from src.application.use_case.subject_class.update_subject_class_case import UpdateSubjectClassCase
from src.infrastructure.entities.course.subject_class import SubjectClass
from src.infrastructure.exceptions.except_manager import manage_subject_class_except

class SubjectClassController:
    def __init__(
        self,
        find_case: FindSubjectClassCase,
        create_case: CreateSubjectClassCase,
        update_case: UpdateSubjectClassCase,
        delete_case: DeleteSubjectClassCase,
    ):
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, payload: SubjectClass):
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
            manage_subject_class_except(e)

    async def update(self, payload: SubjectClass):
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
            manage_subject_class_except(e)

    async def delete(self, subject_class_id: int):

        try:
            await self.find_case.get(subject_class_id)
            resp = await self.delete_case.delete(
                subject_class_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_subject_class_except(e)

    async def get(self, subject_class_id: str):
        try:
            resp = await self.find_case.get(subject_class_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_subject_class_except(e)
    
    async def get_all(self):
        try:
            resp = await self.find_case.get_all()
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_subject_class_except(e)
