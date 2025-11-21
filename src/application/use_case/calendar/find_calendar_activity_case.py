from typing import List, Optional
from fastapi import HTTPException, status
from src.infrastructure.entities.course.calendary_activity import CalendarActivity
from src.infrastructure.repositories.calendary_activity import CalendarActivityRepository




class FindCalendarActivityCase:

    def __init__(self, repo: CalendarActivityRepository):
        self.repo = repo

    async def get(self, intolerance_id: int) -> Optional[CalendarActivity]:
        course = await self.repo.get(intolerance_id)
        if course is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Calendar Activity not found"
            )
        return course

    async def get_all(self) -> List[CalendarActivity]:
        return await self.repo.get_all()