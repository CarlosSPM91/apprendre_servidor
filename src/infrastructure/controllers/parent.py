from fastapi import HTTPException
import sentry_sdk
from src.application.use_case.parent.create_parent_case import CreateParentCase
from src.application.use_case.parent.delete_parent_case import DeleteParentCase
from src.application.use_case.parent.find_parent_case import FindParentCase
from src.infrastructure.entities.users.parents import Parent
from src.infrastructure.exceptions.except_manager import manage_parent_except


class ParentController:
    """
    Controller for managing Parent entities.

    Handles interactions between FastAPI endpoints and the parent use cases
    for creating, deleting, and retrieving parents and their associated students.
    """

    def __init__(
        self,
        find_case: FindParentCase,
        create_case: CreateParentCase,
        delete_case: DeleteParentCase,
    ):
        """
        Initialize the ParentController with required use cases.

        Args:
            find_case (FindParentCase): Use case for retrieving parent data.
            create_case (CreateParentCase): Use case for creating a parent.
            delete_case (DeleteParentCase): Use case for deleting a parent.
        """
        self.find_case = find_case
        self.create_case = create_case
        self.delete_case = delete_case

    async def create(self, payload: Parent):
        """
        Create a new parent.

        Args:
            payload (Parent): Parent entity to create.

        Returns:
            dict: Status and created parent info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "deleted_date": str(resp.event_date),
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
                    "deleted_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_parent_except(e)

    async def delete(self, user_id: int, student_id: int):
        """
        Delete a parent-student association.

        Args:
            user_id (int): Parent user ID.
            student_id (int): Student ID.

        Returns:
            dict: Status and deletion info:
                {
                    "status": "success",
                    "data": {
                        "id": str(resp.item_id),
                        "deleted_date": str(resp.event_date),
                    }
                }

        Raises:
            HTTPException: If deletion fails or association not found.
        """
        try:
            resp = await self.delete_case.delete(user_id=user_id, student_id=student_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deleted_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_parent_except(e)

    async def get_parent(self, user_id: int):
        """
        Retrieve a parent by user ID.

        Args:
            user_id (int): Parent's user ID.

        Returns:
            dict: Status and parent data:
                {
                    "status": "success",
                    "data": parent,
                }

        Raises:
            HTTPException: If parent not found.
        """
        try:
            parent = await self.find_case.get(user_id=user_id)
            return {
                "status": "success",
                "data": parent,
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_parent_except(e)

    async def get_all(self):
        """
        Retrieve all parents and their associated students.

        Returns:
            dict: Status and list of parents:
                {
                    "status": "success",
                    "data": parents,
                }

        Raises:
            HTTPException: If retrieval fails.
        """
        try:
            parents = await self.find_case.get_all()
            return {
                "status": "success",
                "data": parents,
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_parent_except(e)
