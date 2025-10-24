from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.medical_info.create_medical_case import CreateMedicalCase
from src.application.use_case.medical_info.delete_medical_case import DeleteMedicalCase
from src.application.use_case.medical_info.find_medical_case import FindMedicalCase
from src.application.use_case.medical_info.update_medical_case import UpdateMedicalCase
from src.infrastructure.entities.student_info.medical_info import MedicalInfo
from src.infrastructure.exceptions.except_manager import manage_medical_except

class MedicalInfoController:
    def __init__(
        self,
        find_case: FindMedicalCase,
        create_case: CreateMedicalCase,
        update_case: UpdateMedicalCase,
        delete_case: DeleteMedicalCase,
    ):
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, medical: MedicalInfo):
        try:
            resp = await self.create_case.create(medical)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "created_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_medical_except(e)

    async def update(self, payload: MedicalInfo):
        try:
            await self.find_case.get_medical(payload.id)
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
            manage_medical_except(e)

    async def delete(self, medical_id: int):

        try:
            await self.find_case.get_medical(medical_id)
            resp = await self.delete_case.delete(
                medical_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_medical_except(e)

    async def get_medical (self, medical_id: str):
        try:
            resp = await self.find_case.get_medical(medical_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_medical_except(e)
    
    async def get_all(self):
        try:
            resp = await self.find_case.get_all()
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_medical_except(e)
