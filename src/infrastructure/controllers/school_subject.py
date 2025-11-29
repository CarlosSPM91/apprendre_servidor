from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.school_subject.create_school_subject_case import CreateSchoolSubjectCase
from src.application.use_case.school_subject.delete_school_subject_case import DeleteSchoolSubjectCase
from src.application.use_case.school_subject.find_school_subject_case import FindSchoolSubjectCase
from src.application.use_case.school_subject.update_school_subject_case import UpdateSchoolSubjectCase
from src.infrastructure.entities.course.school_subject import SchoolSubject
from src.infrastructure.exceptions.except_manager import manage_school_subject_except

class SchoolSubjectController:
    def __init__(
        self,
        find_case: FindSchoolSubjectCase,
        create_case: CreateSchoolSubjectCase,
        update_case: UpdateSchoolSubjectCase,
        delete_case: DeleteSchoolSubjectCase,
    ):
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, payload: SchoolSubject):
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
            manage_school_subject_except(e)

    async def update(self, payload: SchoolSubject):
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
            manage_school_subject_except(e)

    async def delete(self, school_subject_id: int):

        try:
            await self.find_case.get(school_subject_id)
            resp = await self.delete_case.delete(
                school_subject_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_school_subject_except(e)

    async def get(self, school_subject_id: str):
        try:
            resp = await self.find_case.get(school_subject_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_school_subject_except(e)
    
    async def get_all(self):
        try:
            resp = await self.find_case.get_all()
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_school_subject_except(e)
