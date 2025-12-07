from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.subject_class.create_subject_class_case import CreateSubjectClassCase
from src.application.use_case.subject_class.delete_subject_class_case import DeleteSubjectClassCase
from src.application.use_case.subject_class.find_subject_class_case import FindSubjectClassCase
from src.application.use_case.subject_class.update_subject_class_case import UpdateSubjectClassCase
from src.infrastructure.entities.course.subject_class import SubjectClass
from src.infrastructure.exceptions.except_manager import manage_subject_class_except

"""
SubjectClassController.

Handles HTTP requests related to SubjectClass entity and delegates to use case layer.

:author: Carlos S. Paredes Morillo
"""

class SubjectClassController:
    """Controller for SubjectClass operations.

    Provides methods to create, update, delete, and retrieve subject-class records.
    Handles exceptions and reports them to Sentry.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(
        self,
        find_case: FindSubjectClassCase,
        create_case: CreateSubjectClassCase,
        update_case: UpdateSubjectClassCase,
        delete_case: DeleteSubjectClassCase,
    ):
        """Initialize the controller with use case dependencies.

        Args:
            find_case (FindSubjectClassCase): Use case for finding subject-class records.
            create_case (CreateSubjectClassCase): Use case for creating subject-class records.
            update_case (UpdateSubjectClassCase): Use case for updating subject-class records.
            delete_case (DeleteSubjectClassCase): Use case for deleting subject-class records.
        """
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, payload: SubjectClass):
        """Create a new subject-class record.

        Args:
            payload (SubjectClass): SubjectClass entity to create.

        Returns:
            dict: Success status and created subject-class data.

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
            manage_subject_class_except(e)

    async def update(self, payload: SubjectClass):
        """Update an existing subject-class record.

        Args:
            payload (SubjectClass): SubjectClass entity with updated data.

        Returns:
            dict: Success status and updated subject-class data.

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
            manage_subject_class_except(e)

    async def delete(self, subject_class_id: int):
        """Delete a subject-class record by ID.

        Args:
            subject_class_id (int): ID of the subject-class record to delete.

        Returns:
            dict: Success status and deletion data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            await self.find_case.get(subject_class_id)
            resp = await self.delete_case.delete(subject_class_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_subject_class_except(e)

    async def get(self, subject_class_id: str):
        """Retrieve a subject-class record by ID.

        Args:
            subject_class_id (str): ID of the subject-class record.

        Returns:
            dict: Success status and retrieved subject-class data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            resp = await self.find_case.get(subject_class_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_subject_class_except(e)

    async def get_all(self):
        """Retrieve all subject-class records.

        Returns:
            dict: Success status and list of all subject-class records.

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
            manage_subject_class_except(e)
