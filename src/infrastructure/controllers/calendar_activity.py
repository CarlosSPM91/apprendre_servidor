from typing import List
from fastapi import HTTPException
import sentry_sdk

from src.application.use_case.calendar.create_calendar_activity_case import CreateCalendarActivityCase
from src.application.use_case.calendar.delete_calendar_activity_case import DeleteCalendarActivityCase
from src.application.use_case.calendar.find_calendar_activity_case import FindCalendarActivityCase
from src.application.use_case.calendar.update_calendar_activity_case import UpdateCalendarActivityCase
from src.infrastructure.entities.course.calendary_activity import CalendarActivity
from src.infrastructure.exceptions.except_manager import manage_calendar_except

class CalendarController:
    def __init__(
        self,
        find_case: FindCalendarActivityCase,
        create_case: CreateCalendarActivityCase,
        update_case: UpdateCalendarActivityCase,
        delete_case: DeleteCalendarActivityCase,
    ):
        self.find_case = find_case
        self.create_case = create_case
        self.update_case = update_case
        self.delete_case = delete_case

    async def create(self, calendar: CalendarActivity):
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

        try:
            await self.find_case.get(calendar_activity_id)
            resp = await self.delete_case.delete(
                calendar_activity_id)
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
        try:
            resp = await self.find_case.get_all()
            return {
                "status": "success",
                "data": resp
            }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_calendar_except(e)
