from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.classes.create_classes_case import CreateClassesCase
from src.application.use_case.classes.delete_classes_case import DeleteClassesCase
from src.application.use_case.classes.find_classes_case import FindClassesCase
from src.application.use_case.classes.update_classes_case import UpdateClassesCase
from src.domain.objects.classes.update_class_subjects_dto import UpdateClassSubjectsDTO
from src.infrastructure.entities.course.classes import Classes
from src.infrastructure.exceptions.except_manager import manage_classes_except

class ClassesController:
    def __init__(
        self,
        find_case: FindClassesCase,
        create_case: CreateClassesCase,
        update_case: UpdateClassesCase,
        delete_case: DeleteClassesCase,
    ):
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, classes: Classes):
        try:
            resp = await self.create_case.create(classes)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "created_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_classes_except(e)

    async def update(self, payload: Classes):
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
            manage_classes_except(e)
    
    async def update_subjects(self, payload: UpdateClassSubjectsDTO):
        try:
            await self.find_case.get(payload.class_id)
            resp = await self.update_case.update_subjects(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "updated_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_classes_except(e)

    async def delete(self, classes_id: int):

        try:
            await self.find_case.get(classes_id)
            resp = await self.delete_case.delete(
                classes_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_classes_except(e)

    async def get(self, classes_id: str):
        try:
            resp = await self.find_case.get(classes_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_classes_except(e)
    
    async def get_all(self):
        try:
            resp = await self.find_case.get_all()
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_classes_except(e)
