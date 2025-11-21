
from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.course.calendary_activity import CalendarActivity
from src.infrastructure.repositories.calendary_activity import CalendarActivityRepository



class UpdateCalendarActivityCase:

    def __init__(self,repo: CalendarActivityRepository):
        self.repo = repo

    async def update(self, payload: CalendarActivity) -> CommonResponse:
        course = await self.repo.update(payload)
        if course:
            return CommonResponse(
                item_id=course.id,
                event_date=datetime.now(timezone.utc)
            )