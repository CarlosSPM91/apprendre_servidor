from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.course.create_course_case import CreateCourseCase
from src.application.use_case.course.delete_course_case import DeleteCourseCase
from src.application.use_case.course.find_course_case import FindCourseCase
from src.application.use_case.course.update_course_case import UpdateCourseCase
from src.infrastructure.entities.course.course import Course
from src.infrastructure.exceptions.except_manager import manage_course_except

class CourseController:
    def __init__(
        self,
        find_case: FindCourseCase,
        create_case: CreateCourseCase,
        update_case: UpdateCourseCase,
        delete_case: DeleteCourseCase,
    ):
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, course: Course):
        try:
            resp = await self.create_case.create(course)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "created_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_course_except(e)

    async def update(self, payload: Course):
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
            manage_course_except(e)

    async def delete(self, course_id: int):

        try:
            await self.find_case.get(course_id)
            resp = await self.delete_case.delete(
                course_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_course_except(e)

    async def get(self, course_id: str):
        try:
            resp = await self.find_case.get(course_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_course_except(e)
    
    async def get_all(self):
        try:
            resp = await self.find_case.get_all()
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_course_except(e)
