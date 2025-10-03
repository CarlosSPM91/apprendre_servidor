
import datetime
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.user import UserRepository


class DeleteUserCase:
    async def __init__(self, repo: UserRepository):
        self.userRepo = repo

    async def delete(
        self,
        user_id:str,
    ) -> CommonResponse:
        resp= self.userRepo.delete(user_id)
        if resp:
            return CommonResponse(
                user_id=user_id,
                delete_date=datetime.now(datetime.timezone.utc)
            )