from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.student_class.create_student_class_case import CreateStudentClassCase
from src.application.use_case.student_class.delete_student_class_case import DeleteStudentClassCase
from src.application.use_case.student_class.find_student_class_case import FindStudentClassCase
from src.application.use_case.student_class.update_student_class_case import UpdateStudentClassCase
from src.infrastructure.entities.course.student_class import StudentClass
from src.infrastructure.exceptions.except_manager import manage_student_class_except

"""
StudentClassController.

Handles HTTP requests related to StudentClass entity and delegates to use case layer.

:author: Carlos S. Paredes Morillo
"""

class StudentClassController:
    """Controller for StudentClass operations.

    Provides methods to create, update points, delete, and retrieve student-class relations.
    Handles exceptions and reports them to Sentry.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(
        self,
        find_case: FindStudentClassCase,
        create_case: CreateStudentClassCase,
        update_case: UpdateStudentClassCase,
        delete_case: DeleteStudentClassCase,
    ):
        """Initialize the controller with use case dependencies.

        Args:
            find_case (FindStudentClassCase): Use case for finding student-class records.
            create_case (CreateStudentClassCase): Use case for creating student-class records.
            update_case (UpdateStudentClassCase): Use case for updating student-class points.
            delete_case (DeleteStudentClassCase): Use case for deleting student-class records.
        """
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, payload: StudentClass):
        """Create a new student-class record.

        Args:
            payload (StudentClass): StudentClass entity to create.

        Returns:
            dict: Success status and created student-class data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
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
            manage_student_class_except(e)

    async def update_points(self, payload: StudentClass):
        """Update points for an existing student-class record.

        Args:
            payload (StudentClass): StudentClass entity with updated points.

        Returns:
            dict: Success status and updated student-class data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            await self.find_case.get(payload.id)
            resp = await self.update_case.update_points(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "updated_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_class_except(e)

    async def delete(self, student_class_id: int):
        """Delete a student-class record by ID.

        Args:
            student_class_id (int): ID of the student-class record to delete.

        Returns:
            dict: Success status and deletion data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            await self.find_case.get(student_class_id)
            resp = await self.delete_case.delete(student_class_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_class_except(e)

    async def get(self, student_class_id: str):
        """Retrieve a student-class record by ID.

        Args:
            student_class_id (str): ID of the student-class record.

        Returns:
            dict: Success status and retrieved student-class data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            resp = await self.find_case.get(student_class_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_student_class_except(e)
    
    async def get_all(self):
        """Retrieve all student-class records.

        Returns:
            dict: Success status and list of all student-class records.

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
            manage_student_class_except(e)
