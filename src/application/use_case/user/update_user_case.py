from datetime import timezone
import datetime

from fastapi import HTTPException, status
from src.application.services.password_service import PasswordService
from src.domain.objects.auth.pwd_req import PasswordRequest
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.user.user_dto import UserDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.repositories.user import UserRepository


class UpdateUserCase:
    async def __init__(self, pwd_service: PasswordService, repo: UserRepository):
        self.pwdService = pwd_service
        self.userRepo = repo
        
    async def update_user(self, userUpt: UserUpdateDTO) -> CommonResponse:

        user = await self.userRepo.update_user(userUpt)
        if user:
            return CommonResponse(
                item_id=userUpt.user_id,
                event_date= datetime.now(timezone.utc)
            )
    
    async def update_last_used(self, user_id: int) -> CommonResponse:

        user= await self.userRepo.update_last_used(user_id)
        if user:
                return CommonResponse(
                    item_id=user_id,
                    event_date= datetime.now(timezone.utc)
                )

    async def change_password(self, user: PasswordRequest) -> CommonResponse:
        pwd:str = self.pwdService.hash_password(user.password)
        
        is_changed= await self.userRepo.change_password(user.user_id, pwd)
        if is_changed:
            return CommonResponse(
                item_id=user.user_id,
                event_date= datetime.now(timezone.utc)
            )
