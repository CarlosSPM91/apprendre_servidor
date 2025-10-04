
from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.user import UserRepository


class DeleteUserCase:
    def __init__(self, repo: UserRepository):
        self.userRepo = repo

    async def delete(
        self,
        user_id:int,
    ) -> CommonResponse:
        resp= await self.userRepo.delete(user_id)
        if resp:
            return CommonResponse(
                item_id=user_id,
                event_date=datetime.now(timezone.utc)
            )