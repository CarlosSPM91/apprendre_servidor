import jwt
from fastapi import Depends, HTTPException, status
from src.application.services.password_service import PasswordService
from src.application.services.token_service import TokenService
from datetime import datetime, timedelta, timezone
from src import settings
from src.application.services.user import UserService
from src.domain.objects.auth.login_resp import LoginResponse
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.entities.user import User


class AuthService:
    def __init__(
        self,
        pwd_service: PasswordService,
        token_service: TokenService,
        user_service: UserService,
    ):
        self.pwd_service = pwd_service
        self.token_sevice = token_service
        self.user_service = user_service

    async def login(
        self,
        payload: JwtPayload,
    ) -> LoginResponse:
        hash_pass = self.pwd_service.hash_password(payload.password)

        user: User = self.user_service.getUserByUsermame(payload["username"])

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if user.password != hash_pass:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        jwtPayload = JwtPayload()
        jwtPayload.id = str(user.id)
        jwtPayload.username = user.username
        jwtPayload.name = user.name
        jwtPayload.last_name = user.last_names
        jwtPayload.role = user.role

        token = self.token_service.generate_token(jwtPayload)

        await self.user_service.updateLastUsed(user.id)

        return {
            "acces_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
        }
