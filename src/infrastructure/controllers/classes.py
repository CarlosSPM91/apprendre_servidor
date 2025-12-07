from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.classes.create_classes_case import CreateClassesCase
from src.application.use_case.classes.delete_classes_case import DeleteClassesCase
from src.application.use_case.classes.find_classes_case import FindClassesCase
from src.application.use_case.classes.update_classes_case import UpdateClassesCase
from src.domain.objects.classes.update_class_subjects_dto import UpdateClassSubjectsDTO
from src.infrastructure.entities.course.classes import Classes
from src.infrastructure.exceptions.except_manager import manage_classes_except

"""
ClassesController.

Handles HTTP requests related to Classes entity and delegates to use case layer.

:author: Carlos S. Paredes Morillo
"""

class ClassesController:
    """Controller for Classes operations.

    Provides methods to create, update, delete, and retrieve classes,
    as well as updating class subjects. Handles exceptions and reports them to Sentry.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(
        self,
        find_case: FindClassesCase,
        create_case: CreateClassesCase,
        update_case: UpdateClassesCase,
        delete_case: DeleteClassesCase,
    ):
        """Initialize the controller with use case dependencies.

        Args:
            find_case (FindClassesCase): Use case for finding classes.
            create_case (CreateClassesCase): Use case for creating classes.
            update_case (UpdateClassesCase): Use case for updating classes.
            delete_case (DeleteClassesCase): Use case for deleting classes.
        """
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, classes: Classes):
        """Create a new class.

        Args:
            classes (Classes): Class entity to create.

        Returns:
            dict: Success status and created class data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            resp = await self.create_case.create(classes)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "created_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_classes_except(e)

    async def update(self, payload: Classes):
        """Update an existing class.

        Args:
            payload (Classes): Class entity with updated fields.

        Returns:
            dict: Success status and updated class data.

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
            manage_classes_except(e)
    
    async def update_subjects(self, payload: UpdateClassSubjectsDTO):
        """Update subjects associated with a class.

        Args:
            payload (UpdateClassSubjectsDTO): DTO containing class ID and updated subjects list.

        Returns:
            dict: Success status and updated class subjects data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            await self.find_case.get(payload.class_id)
            resp = await self.update_case.update_subjects(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "updated_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_classes_except(e)

    async def delete(self, classes_id: int):
        """Delete a class by ID.

        Args:
            classes_id (int): ID of the class to delete.

        Returns:
            dict: Success status and deletion data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            await self.find_case.get(classes_id)
            resp = await self.delete_case.delete(classes_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_classes_except(e)

    async def get(self, classes_id: str):
        """Retrieve a class by ID.

        Args:
            classes_id (str): ID of the class.

        Returns:
            dict: Success status and retrieved class data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            resp = await self.find_case.get(classes_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_classes_except(e)
    
    async def get_all(self):
        """Retrieve all classes.

        Returns:
            dict: Success status and list of all classes.

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
            manage_classes_except(e)
