from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.food_intolerance.create_intolerance_case import CreateIntoleranceCase
from src.application.use_case.food_intolerance.delete_intolerance_case import DeleteIntoleranceCase
from src.application.use_case.food_intolerance.find_intolerance_case import FindIntoleranceCase
from src.application.use_case.food_intolerance.update_intolerance_case import UpdateIntoleranceCase
from src.domain.exceptions.except_manager import manage_intolerance_except
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance

class FoodIntoleranceController:
    def __init__(
        self,
        find_case: FindIntoleranceCase,
        create_case: CreateIntoleranceCase,
        update_case: UpdateIntoleranceCase,
        delete_case: DeleteIntoleranceCase,
    ):
        self.find_intolerance_case = find_case
        self.create_intolerance_case = create_case
        self.update_intolerance_case = update_case
        self.delete_intolerance_case = delete_case

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
            manage_intolerance_except(e)

    async def update(self, payload: FoodIntolerance):
        try:
            await self.find_student_case.get_student_by_id(payload.student_id)
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
            manage_intolerance_except(e)

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
            manage_intolerance_except(e)

    async def get_intolerance(self, intolernce_id: str):
        try:
            return await self.find_student_case.get_student_by_id(intolernce_id=intolernce_id)
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_intolerance_except(e)
