from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.course.classes import Classes
from src.infrastructure.repositories.classes import ClassesRepository


class CreateClassesCase:


    def __init__(self, repo: ClassesRepository):
        self.repo = repo

    async def create(self, payload: Classes) -> CommonResponse:
        classes = await self.repo.create(payload)

        return CommonResponse(
            item_id=classes.id,
            event_date=datetime.now(timezone.utc)
        )
