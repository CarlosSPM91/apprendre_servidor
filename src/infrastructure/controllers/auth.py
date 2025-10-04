
from fastapi import HTTPException
from src.application.use_case.auth.login_use_case import LoginUseCase
from src.domain.exceptions.except_manager import manage_auth_except
from src.domain.objects.auth.login_req import LoginRequest


class AuthController:
    def __init__(self, login_case: LoginUseCase):
        self.login_case = login_case

    async def login(
        self,
        payload: LoginRequest,
    ):
        try:
            return await self.login_case.login(payload)
        except HTTPException as e:
            manage_auth_except(e)
