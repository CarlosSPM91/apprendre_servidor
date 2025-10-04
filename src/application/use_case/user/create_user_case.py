from datetime import datetime, timezone

from fastapi import HTTPException, status
from src.application.services.password_service import PasswordService
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_dto import UserDTO
from src.infrastructure.repositories.user import UserRepository


class CreateUserCase:
    def __init__(self, pwd_service: PasswordService, repo: UserRepository):
        self.pwdService = pwd_service
        self.userRepo = repo

    async def create(
        self,
        payload: UserCreateDTO,
    ) -> CommonResponse:
        user_check = await self.userRepo.get_user_by_username(payload.username)
        if user_check:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exist"
            )
        pwd_hash = self.pwdService.hash_password(payload.password)
        payload.password = pwd_hash
        user_created = await self.userRepo.create(payload)
        return CommonResponse(
            item_id=user_created.user_id,
            event_date=datetime.now(timezone.utc)
        )
