from datetime import datetime, timezone
from fastapi import HTTPException, status
from src.application.services.password_service import PasswordService
from src.application.services.token_service import TokenService
from src.application.use_case.user.find_user_case import FindUserCase
from src.application.use_case.user.update_user_case import UpdateUserCase
from src.domain.objects.auth.login_req import LoginRequest
from src.domain.objects.auth.login_resp import LoginResponse
from src.domain.objects.token.jwtPayload import JwtPayload
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.entities.users.accces_logs import AccessLog
from src.infrastructure.repositories.acces_logs import AccessRepository


class LogoutUseCase:
    def __init__(
        self,
        token_service: TokenService,
    ):
        self.token_sevice = token_service

    async def logout(self, user_id:int) -> bool:
        return await self.token_sevice.invalidate_token(user_id)