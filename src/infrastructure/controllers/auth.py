
from fastapi import HTTPException, status
import sentry_sdk
from src.application.use_case.auth.login_use_case import LoginUseCase
from src.application.use_case.auth.logout_use_case import LogoutUseCase
from src.domain.exceptions.except_manager import manage_auth_except
from src.domain.objects.auth.login_req import LoginRequest


class AuthController:
    def __init__(self, login_case: LoginUseCase, logout_case:LogoutUseCase):
        self.login_case = login_case
        self.logout_case = logout_case

    async def login(
        self,
        payload: LoginRequest,
    ):
        try:
            return await self.login_case.login(payload)
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_auth_except(e)

    async def logout(
        self,
        token:str,
    ):
        try:
            is_invalidated= await self.logout_case.logout(token)
            print(is_invalidated)
            if not is_invalidated:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={
                        "message": "Something go wrong"
                    }
                )
            return {
                    "status": "success",
                    "message": "Session closed"
                }
        except HTTPException as e:
            sentry_sdk.capture_exception(e)
            manage_auth_except(e)