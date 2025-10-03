from typing import Container
from fastapi import Depends
from src.application.use_case.auth.login_use_case import LoginUseCase
from src.container import Container
from dependency_injector.wiring import Provide
from src.domain.objects.auth.login_req import LoginRequest

class AuthController:
    def __init__(self):
        pass

    async def login(
            self,
            payload:LoginRequest,
            login_case: LoginUseCase = Depends(Provide[Container.auth_service]),
    ):
            return await login_case.login(payload)



    


    
