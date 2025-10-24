from typing import List
from fastapi import HTTPException
import sentry_sdk


from src.application.use_case.allergy_info.create_allergy_case import CreateAllergyCase
from src.application.use_case.allergy_info.delete_allergy_case import DeleteAllergyCase
from src.application.use_case.allergy_info.find_allergy_case import FindAllergyCase
from src.application.use_case.allergy_info.update_allergy_case import UpdateAllergyCase
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.infrastructure.exceptions.except_manager import manage_allergy_except

class AllergyController:
    def __init__(
        self,
        find_case: FindAllergyCase,
        create_case: CreateAllergyCase,
        update_case: UpdateAllergyCase,
        delete_case: DeleteAllergyCase,
    ):
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, payload: AllergyInfo):
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
            manage_allergy_except(e)

    async def update(self, payload: AllergyInfo):
        try:
            await self.find_case.get_allergy(payload.id)
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
            manage_allergy_except(e)

    async def delete(self, allergy_id: int):

        try:
            await self.find_case.get_allergy(allergy_id)
            resp = await self.delete_case.delete(
                allergy_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_allergy_except(e)

    async def get_allergy (self, allergy_id: str):
        try:
            resp= await self.find_case.get_allergy(allergy_id)

            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_allergy_except(e)

    async def get_all(self):
        try:
            resp = await self.find_case.get_all()
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_allergy_except(e)
