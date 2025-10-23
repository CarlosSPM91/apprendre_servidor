from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.teacher import TeacherRepository



class CreateTeacherCase:


    def __init__(self, repo: TeacherRepository):
        self.repo = repo

    async def create(self, user_id: int) -> CommonResponse:
        resp = await self.repo.create(user_id=user_id)

        return CommonResponse(
            item_id=resp.id,
            event_date=datetime.now(timezone.utc)
        )
