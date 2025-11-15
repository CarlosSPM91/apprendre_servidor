from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.student.create_student_case import CreateStudenCase
from src.application.use_case.student.delete_student_case import DeleteStudentCase
from src.application.use_case.student.find_student_case import FindStudentCase
from src.application.use_case.student.update_student_case import UpdateStudentCase
from src.domain.objects.profiles.student_update_dto import StudentUpdateDTO
from src.infrastructure.exceptions.except_manager import manage_student_except


class StudentController:
    """
    Controller for managing Student entities.

    Handles the interaction between FastAPI endpoints and the student
    use cases for creating, updating, deleting, and retrieving students.
    """

    def __init__(
        self,
        find_case: FindStudentCase,
        create_case: CreateStudenCase,
        update_case: UpdateStudentCase,
        delete_case: DeleteStudentCase,
    ):
        """
        Initialize the StudentController with the required use cases.

        Args:
            find_case (FindStudentCase): Use case for retrieving student data.
            create_case (CreateStudenCase): Use case for creating a student.
            update_case (UpdateStudentCase): Use case for updating a student.
            delete_case (DeleteStudentCase): Use case for deleting a student.
        """
        self.find_student_case = find_case
        self.create_student_case = create_case
        self.update_student_case = update_case
        self.delete_student_case = delete_case

    async def create(self, user_id: int):
        """
        Create a new student for a given user ID.

        Args:
            user_id (int): ID of the user to create a student record for.

        Returns:
            dict: Contains status and the created student info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "created_date": str(resp.event_date),
                    }
                }

        Raises:
            HTTPException: If creation fails, captured and managed by Sentry.
        """
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
            manage_student_except(e)

    async def update(self, payload: StudentUpdateDTO):
        """
        Update an existing student.

        Args:
            payload (StudentUpdateDTO): DTO containing student ID and updated fields.

        Returns:
            dict: Contains status and updated student info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "updated_date": str(resp.event_date),
                    }
                }

        Raises:
            HTTPException: If update fails or student not found.
        """
        try:
            await self.find_student_case.get_student_by_id(student_id=payload.student_id)
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
            manage_student_except(e)

    async def delete(self, student_id: int):
        """
        Delete a student by ID.

        Args:
            student_id (int): ID of the student to delete.

        Returns:
            dict: Contains status and deletion info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "deletion_date": str(resp.event_date),
                    }
                }

        Raises:
            HTTPException: If deletion fails or student not found.
        """
        try:
            await self.find_student_case.get_student_by_id(student_id=student_id)
            resp = await self.delete_student_case.delete(student_id=student_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_except(e)

    async def get_student(self, student_id: str):
        """
        Retrieve a student by ID.

        Args:
            student_id (str): ID of the student.

        Returns:
            dict: Contains status and student data:
                {
                    "status": "success",
                    "data": resp
                }

        Raises:
            HTTPException: If student not found.
        """
        try:
            resp = await self.find_student_case.get_student_by_id(student_id=student_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_except(e)

    async def get_all(self):
        """
        Retrieve all students.

        Returns:
            dict: Contains status and a list of all students:
                {
                    "status": "success",
                    "data": resp
                }

        Raises:
            HTTPException: If retrieval fails.
        """
        try:
            resp = await self.find_student_case.get_all()
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_except(e)

    async def get_student_full_info(self, student_id: int):
        """
        Retrieve full information for a specific student, including related data.

        Args:
            student_id (int): ID of the student.

        Returns:
            dict: Contains status and student full info:
                {
                    "status": "success",
                    "data": resp
                }

        Raises:
            HTTPException: If retrieval fails.
        """
        try:
            resp = await self.find_student_case.get_student_full_info(student_id=student_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_except(e)
