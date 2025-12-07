from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.calendar.create_calendar_activity_case import CreateCalendarActivityCase
from src.application.use_case.calendar.delete_calendar_activity_case import DeleteCalendarActivityCase
from src.application.use_case.calendar.find_calendar_activity_case import FindCalendarActivityCase
from src.application.use_case.calendar.update_calendar_activity_case import UpdateCalendarActivityCase
from src.infrastructure.entities.course.calendary_activity import CalendarActivity
from src.infrastructure.exceptions.except_manager import manage_calendar_except

"""
CalendarController.

Handles HTTP requests related to CalendarActivity entity and delegates to use case layer.

:author: Carlos S. Paredes Morillo
"""

class CalendarController:
    """Controller for CalendarActivity operations.

    Provides methods to create, update, delete, and retrieve calendar activities,
    while handling exceptions and reporting them to Sentry.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(
        self,
        find_case: FindCalendarActivityCase,
        create_case: CreateCalendarActivityCase,
        update_case: UpdateCalendarActivityCase,
        delete_case: DeleteCalendarActivityCase,
    ):
        """Initialize the controller with use case dependencies.

        Args:
            find_case (FindCalendarActivityCase): Use case for finding calendar activities.
            create_case (CreateCalendarActivityCase): Use case for creating calendar activities.
            update_case (UpdateCalendarActivityCase): Use case for updating calendar activities.
            delete_case (DeleteCalendarActivityCase): Use case for deleting calendar activities.
        """
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, calendar: CalendarActivity):
        """Create a new calendar activity.

        Args:
            calendar (CalendarActivity): Calendar activity to create.

        Returns:
            dict: Success status and created activity data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            resp = await self.create_case.create(calendar)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "created_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_calendar_except(e)

    async def update(self, payload: CalendarActivity):
        """Update an existing calendar activity.

        Args:
            payload (CalendarActivity): Calendar activity with updated fields.

        Returns:
            dict: Success status and updated activity data.

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
            manage_calendar_except(e)

    async def delete(self, calendar_activity_id: int):
        """Delete a calendar activity by ID.

        Args:
            calendar_activity_id (int): ID of the calendar activity to delete.

        Returns:
            dict: Success status and deletion data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            await self.find_case.get(calendar_activity_id)
            resp = await self.delete_case.delete(calendar_activity_id)
            return {
                "status": "success",
                "data": {
                    "id": str(resp.item_id),
                    "deletion_date": str(resp.event_date),
                },
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_calendar_except(e)

    async def get(self, calendar_activity_id: str):
        """Retrieve a calendar activity by ID.

        Args:
            calendar_activity_id (str): ID of the calendar activity.

        Returns:
            dict: Success status and retrieved activity data.

        Raises:
            HTTPException: Propagates exceptions from the use case.
        """
        try:
            resp = await self.find_case.get(calendar_activity_id)
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_calendar_except(e)

    async def get_all(self):
        """Retrieve all calendar activities.

        Returns:
            dict: Success status and list of all calendar activities.

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
            manage_calendar_except(e)
