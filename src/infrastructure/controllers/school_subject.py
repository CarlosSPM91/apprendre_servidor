from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.school_subject.create_school_subject_case import CreateSchoolSubjectCase
from src.application.use_case.school_subject.delete_school_subject_case import DeleteSchoolSubjectCase
from src.application.use_case.school_subject.find_school_subject_case import FindSchoolSubjectCase
from src.application.use_case.school_subject.update_school_subject_case import UpdateSchoolSubjectCase
from src.infrastructure.entities.course.school_subject import SchoolSubject
from src.infrastructure.exceptions.except_manager import manage_school_subject_except

"""
SchoolSubjectController.

Handles HTTP requests related to SchoolSubject entity and delegates to use case layer.

:author: Carlos S. Paredes Morillo
"""

class SchoolSubjectController:
    """Controller for SchoolSubject operations.

    Provides methods to create, update, delete, and retrieve school subjects.
    Handles exceptions and reports them to Sentry.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(
        self,
        find_case: FindSchoolSubjectCase,
        create_case: CreateSchoolSubjectCase,
        update_case: UpdateSchoolSubjectCase,
        delete_case: DeleteSchoolSubjectCase,
    ):
        """Initialize the controller with use case dependencies.

        Args:
            find_case (FindSchoolSubjectCase): Use case for finding school subjects.
            create_case (CreateSchoolSubjectCase): Use case for creating school subjects.
            update_case (UpdateSchoolSubjectCase): Use case for updating school subjects.
            delete_case (DeleteSchoolSubjectCase): Use case for deleting school subjects.
        """
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, payload: SchoolSubject):
        """Create a new school subject.

        Args:
            payload (SchoolSubject): SchoolSubject entity to create.

        Returns:
            dict: Success status and created school subject data.

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
            manage_school_subject_except(e)

    async def update(self, payload: SchoolSubject):
        """Update an existing school subject.

        Args:
            payload (SchoolSubject): SchoolSubject entity with updated fields.

        Returns:
            dict: Success status and updated school subject data.

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
            manage_school_subject_except(e)

    async def delete(self, school_subject_id: int):
        """Delete a school subject by ID.

        Args:
            school_subject_id (int): ID of the school subject to delete.

        Returns:
            dict: Success status and deletion data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            await self.find_case.get(school_subject_id)
            resp = await self.delete_case.delete(school_subject_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_school_subject_except(e)

    async def get(self, school_subject_id: str):
        """Retrieve a school subject by ID.

        Args:
            school_subject_id (str): ID of the school subject.

        Returns:
            dict: Success status and retrieved school subject data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            resp = await self.find_case.get(school_subject_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_school_subject_except(e)
    
    async def get_all(self):
        """Retrieve all school subjects.

        Returns:
            dict: Success status and list of all school subjects.

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
            manage_school_subject_except(e)
