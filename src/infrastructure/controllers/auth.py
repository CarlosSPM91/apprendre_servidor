from typing import Container
from fastapi import Depends, HTTPException, status
from src.application.services.auth_service import AuthService
from src.container import Container
from dependency_injector.wiring import Provide
from src.domain.objects.auth.login_req import LoginRequest

class AuthController:
    def __init__(self):
        pass

    async def login(
            self,
            payload:LoginRequest,
            auth_service: AuthService = Depends(Provide[Container.auth_service]),
    ):
            return await auth_service.login(payload)



    


    
