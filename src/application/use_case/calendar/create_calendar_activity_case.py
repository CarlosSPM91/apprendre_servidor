from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.course.calendary_activity import CalendarActivity
from src.infrastructure.repositories.calendary_activity import CalendarActivityRepository


class CreateCalendarActivityCase:


    def __init__(self, repo: CalendarActivityRepository):
        self.repo = repo

    async def create(self, payload: CalendarActivity) -> CommonResponse:
        created = await self.repo.create(payload)

        return CommonResponse(
            item_id=created.id,
            event_date=datetime.now(timezone.utc)
        )