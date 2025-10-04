from typing import Container
from fastapi import Depends
from src.application.use_case.auth.login_use_case import LoginUseCase
from dependency_injector.wiring import Provide
from src.domain.objects.auth.login_req import LoginRequest

class AuthController:
    def __init__(self, login_case: LoginUseCase):
        self.login_case = login_case

    async def login(
            self,
            payload:LoginRequest,
    ):
            return await self.login_case.login(payload)



    


    
