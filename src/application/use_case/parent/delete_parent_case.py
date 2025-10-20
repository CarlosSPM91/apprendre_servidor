from datetime import datetime, timezone
from src.application.use_case.parent.find_parent_case import FindParentCase
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.parent import ParentRepository


class DeleteParentCase:
    def __init__(
        self,
        repo: ParentRepository,
    ):
        self.repo = repo

    async def delete(self, user_id: int, student_id: int) -> bool:
        parent = await self.repo.get(user_id)
        await self.repo.delete(user_id, student_id)
        return CommonResponse(
            item_id=parent.id,
            event_date=datetime.now(timezone.utc)
        )
