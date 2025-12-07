from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.course.create_course_case import CreateCourseCase
from src.application.use_case.course.delete_course_case import DeleteCourseCase
from src.application.use_case.course.find_course_case import FindCourseCase
from src.application.use_case.course.update_course_case import UpdateCourseCase
from src.infrastructure.entities.course.course import Course
from src.infrastructure.exceptions.except_manager import manage_course_except

"""
CourseController.

Handles HTTP requests related to Course entity and delegates to use case layer.

:author: Carlos S. Paredes Morillo
"""

class CourseController:
    """Controller for Course operations.

    Provides methods to create, update, delete, and retrieve courses.
    Handles exceptions and reports them to Sentry.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(
        self,
        find_case: FindCourseCase,
        create_case: CreateCourseCase,
        update_case: UpdateCourseCase,
        delete_case: DeleteCourseCase,
    ):
        """Initialize the controller with use case dependencies.

        Args:
            find_case (FindCourseCase): Use case for finding courses.
            create_case (CreateCourseCase): Use case for creating courses.
            update_case (UpdateCourseCase): Use case for updating courses.
            delete_case (DeleteCourseCase): Use case for deleting courses.
        """
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, course: Course):
        """Create a new course.

        Args:
            course (Course): Course entity to create.

        Returns:
            dict: Success status and created course data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
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
        """Update an existing course.

        Args:
            payload (Course): Course entity with updated fields.

        Returns:
            dict: Success status and updated course data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
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
        """Delete a course by ID.

        Args:
            course_id (int): ID of the course to delete.

        Returns:
            dict: Success status and deletion data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            await self.find_case.get(course_id)
            resp = await self.delete_case.delete(course_id)
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
        """Retrieve a course by ID.

        Args:
            course_id (str): ID of the course.

        Returns:
            dict: Success status and retrieved course data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
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
        """Retrieve all courses.

        Returns:
            dict: Success status and list of all courses.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            resp = await self.find_case.get_all()
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_course_except(e)
