from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.allergy_info.create_allergy_case import CreateAllergyCase
from src.application.use_case.allergy_info.delete_allergy_case import DeleteAllergyCase
from src.application.use_case.allergy_info.find_allergy_case import FindAllergyCase
from src.application.use_case.allergy_info.update_allergy_case import UpdateAllergyCase
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.infrastructure.exceptions.except_manager import manage_allergy_except


class AllergyController:
    """
    Controller for managing AllergyInfo entities.

    Handles interactions between FastAPI endpoints and the allergy use cases
    for creating, updating, deleting, and retrieving allergy records.
    """

    def __init__(
        self,
        find_case: FindAllergyCase,
        create_case: CreateAllergyCase,
        update_case: UpdateAllergyCase,
        delete_case: DeleteAllergyCase,
    ):
        """
        Initialize the AllergyController with required use cases.

        Args:
            find_case (FindAllergyCase): Use case for retrieving allergy info.
            create_case (CreateAllergyCase): Use case for creating allergy info.
            update_case (UpdateAllergyCase): Use case for updating allergy info.
            delete_case (DeleteAllergyCase): Use case for deleting allergy info.
        """
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, payload: AllergyInfo):
        """
        Create a new allergy record.

        Args:
            payload (AllergyInfo): Allergy entity to create.

        Returns:
            dict: Status and created allergy info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "created_date": str(resp.event_date),
                    }
                }

        Raises:
            HTTPException: If creation fails, captured and sent to Sentry.
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
            manage_allergy_except(e)

    async def update(self, payload: AllergyInfo):
        """
        Update an existing allergy record.

        Args:
            payload (AllergyInfo): Allergy entity with updated information.

        Returns:
            dict: Status and updated allergy info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "updated_date": str(resp.event_date),
                    }
                }

        Raises:
            HTTPException: If the allergy record does not exist or update fails.
        """
        try:
            await self.find_case.get_allergy(payload.id)
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
            manage_allergy_except(e)

    async def delete(self, allergy_id: int):
        """
        Delete an allergy record.

        Args:
            allergy_id (int): ID of the allergy record to delete.

        Returns:
            dict: Status and deleted allergy info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "deletion_date": str(resp.event_date),
                    }
                }

        Raises:
            HTTPException: If the allergy record does not exist or deletion fails.
        """
        try:
            await self.find_case.get_allergy(allergy_id)
            resp = await self.delete_case.delete(allergy_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_allergy_except(e)

    async def get_allergy(self, allergy_id: str):
        """
        Retrieve a single allergy record by ID.

        Args:
            allergy_id (str): Allergy record ID.

        Returns:
            dict: Status and allergy record data:
                {
                    "status": "success",
                    "data": resp
                }

        Raises:
            HTTPException: If allergy record not found.
        """
        try:
            resp = await self.find_case.get_allergy(allergy_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_allergy_except(e)

    async def get_all(self):
        """
        Retrieve all allergy records.

        Returns:
            dict: Status and list of all allergy records:
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
            manage_allergy_except(e)
