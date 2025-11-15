from datetime import datetime, timezone

from fastapi import HTTPException, status
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
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent not found"
            )
        await self.repo.delete(user_id=user_id, student_id=student_id)
        return CommonResponse(
            item_id=user_id,
            event_date=datetime.now(timezone.utc)
        )
