from fastapi import HTTPException
import sentry_sdk
from src.application.use_case.teacher.create_teacher_case import CreateTeacherCase
from src.application.use_case.teacher.delete_teacher_case import DeleteTeacherCase
from src.application.use_case.teacher.find_teacher_case import FindTeacherCase
from src.infrastructure.exceptions.except_manager import manage_teacher_except


class TeacherController:
    """
    Controller for managing Teacher entities.

    Handles the interaction between FastAPI endpoints and the application
    use cases for creating, deleting, and retrieving teachers.
    """

    def __init__(
        self,
        find_case: FindTeacherCase,
        create_case: CreateTeacherCase,
        delete_case: DeleteTeacherCase,
    ):
        """
        Initialize the TeacherController with the required use cases.

        Args:
            find_case (FindTeacherCase): Use case for retrieving teacher data.
            create_case (CreateTeacherCase): Use case for creating a teacher.
            delete_case (DeleteTeacherCase): Use case for deleting a teacher.
        """
        self.find_case = find_case
        self.create_case = create_case
        self.delete_case = delete_case

    async def create(self, user_id: int):
        """
        Create a new teacher for a given user ID.

        Args:
            user_id (int): ID of the user to be promoted to teacher.

        Returns:
            dict: A dictionary containing status and the created teacher's info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "deleted_date": str(resp.event_date)
                    }
                }

        Raises:
            HTTPException: If creation fails, captured and managed by Sentry.
        """
        try:
            resp = await self.create_case.create(user_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deleted_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_teacher_except(e)

    async def delete(self, teacher_id: int):
        """
        Delete a teacher by teacher ID.

        Args:
            teacher_id (int): ID of the teacher to delete.

        Returns:
            dict: A dictionary containing status and deletion info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "deleted_date": str(resp.event_date)
                    }
                }

        Raises:
            HTTPException: If deletion fails, captured and managed by Sentry.
        """
        try:
            resp = await self.delete_case.delete(teacher_id=teacher_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deleted_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_teacher_except(e)

    async def get(self, teacher_id: int):
        """
        Retrieve full information for a specific teacher.

        Args:
            teacher_id (int): ID of the teacher to retrieve.

        Returns:
            dict: A dictionary containing status and teacher data:
                {
                    "status": "success",
                    "data": teacher
                }

        Raises:
            HTTPException: If retrieval fails, captured and managed by Sentry.
        """
        try:
            teacher = await self.find_case.get_teacher_full_info(teacher_id=teacher_id)
            return {
                "status": "success",
                "data": teacher,
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_teacher_except(e)

    async def get_all(self):
        """
        Retrieve all teachers.

        Returns:
            dict: A dictionary containing status and a list of all teachers:
                {
                    "status": "success",
                    "data": resp
                }

        Raises:
            HTTPException: If retrieval fails, captured and managed by Sentry.
        """
        try:
            resp = await self.find_case.get_all()
            return {
                "status": "success",
                "data": resp,
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_teacher_except(e)
