from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.food_intolerance.create_intolerance_case import CreateIntoleranceCase
from src.application.use_case.food_intolerance.delete_intolerance_case import DeleteIntoleranceCase
from src.application.use_case.food_intolerance.find_intolerance_case import FindIntoleranceCase
from src.application.use_case.food_intolerance.update_intolerance_case import UpdateIntoleranceCase
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance
from src.infrastructure.exceptions.except_manager import manage_intolerance_except


class FoodIntoleranceController:
    """
    Controller for managing FoodIntolerance entities.

    Handles interactions between FastAPI endpoints and the food intolerance use cases
    for creating, updating, deleting, and retrieving intolerance records.
    """

    def __init__(
        self,
        find_case: FindIntoleranceCase,
        create_case: CreateIntoleranceCase,
        update_case: UpdateIntoleranceCase,
        delete_case: DeleteIntoleranceCase,
    ):
        """
        Initialize the FoodIntoleranceController with required use cases.

        Args:
            find_case (FindIntoleranceCase): Use case for retrieving intolerance info.
            create_case (CreateIntoleranceCase): Use case for creating intolerance info.
            update_case (UpdateIntoleranceCase): Use case for updating intolerance info.
            delete_case (DeleteIntoleranceCase): Use case for deleting intolerance info.
        """
        self.find_intolerance_case = find_case
        self.create_intolerance_case = create_case
        self.update_intolerance_case = update_case
        self.delete_intolerance_case = delete_case

    async def create(self, intolerance: FoodIntolerance):
        """
        Create a new food intolerance record.

        Args:
            intolerance (FoodIntolerance): Intolerance entity to create.

        Returns:
            dict: Status and created intolerance info:
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
            resp = await self.create_intolerance_case.create(intolerance)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "created_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_intolerance_except(e)

    async def update(self, payload: FoodIntolerance):
        """
        Update an existing food intolerance record.

        Args:
            payload (FoodIntolerance): Intolerance entity with updated information.

        Returns:
            dict: Status and updated intolerance info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "updated_date": str(resp.event_date),
                    }
                }

        Raises:
            HTTPException: If the intolerance record does not exist or update fails.
        """
        try:
            await self.find_intolerance_case.get_intolerance(payload.id)
            resp = await self.update_intolerance_case.update(payload)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "updated_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_intolerance_except(e)

    async def delete(self, intolerance_id: int):
        """
        Delete a food intolerance record.

        Args:
            intolerance_id (int): ID of the intolerance record to delete.

        Returns:
            dict: Status and deleted intolerance info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "deletion_date": str(resp.event_date),
                    }
                }

        Raises:
            HTTPException: If the intolerance record does not exist or deletion fails.
        """
        try:
            await self.find_intolerance_case.get_intolerance(intolerance_id)
            resp = await self.delete_intolerance_case.delete(intolerance_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_intolerance_except(e)

    async def get_intolerance(self, intolerance_id: str):
        """
        Retrieve a single food intolerance record by ID.

        Args:
            intolerance_id (str): Intolerance record ID.

        Returns:
            dict: Status and intolerance record data:
                {
                    "status": "success",
                    "data": resp
                }

        Raises:
            HTTPException: If intolerance record not found.
        """
        try:
            resp = await self.find_intolerance_case.get_intolerance(intolerance_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_intolerance_except(e)

    async def get_all(self):
        """
        Retrieve all food intolerance records.

        Returns:
            dict: Status and list of all intolerance records:
                {
                    "status": "success",
                    "data": resp
                }

        Raises:
            HTTPException: If retrieval fails.
        """
        try:
            resp = await self.find_intolerance_case.get_all()
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_intolerance_except(e)
