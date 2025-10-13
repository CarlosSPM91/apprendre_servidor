"""
Login Use Case.

Handles user login, password verification, token generation, 
and access logging.

:author: Carlos S. Paredes Morillo
"""

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


class LoginUseCase:
    """Use case for handling user login operations."""

    def __init__(
        self,
        pwd_service: PasswordService,
        token_service: TokenService,
        find_case: FindUserCase,
        update_case: UpdateUserCase,
        access_repository: AccessRepository,
    ):
        """
        Initialize the LoginUseCase with required services and repositories.

        Args:
            pwd_service (PasswordService): Service for password hashing.
            token_service (TokenService): Service for JWT token generation and validation.
            find_case (FindUserCase): Use case to find users.
            update_case (UpdateUserCase): Use case to update user data.
            access_repository (AccessRepository): Repository for logging user access events.
        """
        self.pwd_service = pwd_service
        self.token_service = token_service
        self.find_user_case = find_case
        self.update_user_case = update_case
        self.access_repo = access_repository

    async def login(self, payload: LoginRequest) -> LoginResponse:
        """
        Authenticate a user, generate a JWT token, update last login, 
        and log access.

        Args:
            payload (LoginRequest): The login request containing username and password.

        Returns:
            LoginResponse: Contains JWT access token, token type, and user info.

        Raises:
            HTTPException: If the user is not found or the password is invalid.
        """
        hash_pass = self.pwd_service.hash_password(payload.password)

        user: UserUpdateDTO = await self.find_user_case.get_user_by_username(
            payload.username
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if user.password != hash_pass:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        jwtPayload = JwtPayload(
            user_id=str(user.user_id),
            username=user.username,
            name=user.name,
            last_name=user.last_name,
            role=user.role_id,
        )

        token = await self.token_service.generate_token(jwtPayload)

        await self.update_user_case.update_last_used(user.user_id)

        acces = AccessLog(
            user_id=user.user_id,
            username=user.username,
            acces_date=datetime.now(timezone.utc),
        )
        await self.access_repo.create(acces)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": str(user.user_id),
            "username": user.username,
            "role": user.role_id,
        }
