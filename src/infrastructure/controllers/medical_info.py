from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.medical_info.create_medical_case import CreateMedicalCase
from src.application.use_case.medical_info.delete_medical_case import DeleteMedicalCase
from src.application.use_case.medical_info.find_medical_case import FindMedicalCase
from src.application.use_case.medical_info.update_medical_case import UpdateMedicalCase
from src.infrastructure.entities.student_info.medical_info import MedicalInfo
from src.infrastructure.exceptions.except_manager import manage_medical_except


class MedicalInfoController:
    """
    Controller for managing MedicalInfo entities.

    Handles the creation, updating, deletion, and retrieval of medical information
    for students, coordinating between FastAPI endpoints and use cases.
    """

    def __init__(
        self,
        find_case: FindMedicalCase,
        create_case: CreateMedicalCase,
        update_case: UpdateMedicalCase,
        delete_case: DeleteMedicalCase,
    ):
        """
        Initialize the MedicalInfoController with required use cases.

        Args:
            find_case (FindMedicalCase): Use case for retrieving medical info.
            create_case (CreateMedicalCase): Use case for creating medical info.
            update_case (UpdateMedicalCase): Use case for updating medical info.
            delete_case (DeleteMedicalCase): Use case for deleting medical info.
        """
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, medical: MedicalInfo):
        """
        Create a new medical info record.

        Args:
            medical (MedicalInfo): Medical info entity to create.

        Returns:
            dict: Status and created medical info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "created_date": str(resp.event_date),
                    }
                }

        Raises:
            HTTPException: If creation fails.
        """
        try:
            resp = await self.create_case.create(medical)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "created_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_medical_except(e)

    async def update(self, payload: MedicalInfo):
        """
        Update an existing medical info record.

        Args:
            payload (MedicalInfo): Medical info entity with updated information.

        Returns:
            dict: Status and updated medical info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "updated_date": str(resp.event_date),
                    }
                }

        Raises:
            HTTPException: If the medical info record does not exist or update fails.
        """
        try:
            await self.find_case.get_medical(payload.id)
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
            manage_medical_except(e)

    async def delete(self, medical_id: int):
        """
        Delete a medical info record.

        Args:
            medical_id (int): ID of the medical info record to delete.

        Returns:
            dict: Status and deleted medical info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "deletion_date": str(resp.event_date),
                    }
                }

        Raises:
            HTTPException: If the medical info record does not exist or deletion fails.
        """
        try:
            await self.find_case.get_medical(medical_id)
            resp = await self.delete_case.delete(medical_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_medical_except(e)

    async def get_medical(self, medical_id: str):
        """
        Retrieve a single medical info record by ID.

        Args:
            medical_id (str): Medical info record ID.

        Returns:
            dict: Status and medical info record data:
                {
                    "status": "success",
                    "data": resp
                }

        Raises:
            HTTPException: If medical info record not found.
        """
        try:
            resp = await self.find_case.get_medical(medical_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_medical_except(e)

    async def get_all(self):
        """
        Retrieve all medical info records.

        Returns:
            dict: Status and list of all medical info records:
                {
                    "status": "success",
                    "data": resp
                }

        Raises:
            HTTPException: If retrieval fails.
        """
        try:
            resp = await self.find_case.get_all()
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_medical_except(e)
