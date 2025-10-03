from fastapi import HTTPException, status
from src.application.services.password_service import PasswordService
from src.application.services.token_service import TokenService
from src.application.use_case.user.find_user_case import FindUserCase
from src.application.use_case.user.update_user_case import UpdateUserCase
from src.domain.objects.auth.login_resp import LoginResponse
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.entities.user import User


class LoginUseCase:
    def __init__(
        self,
        pwd_service: PasswordService,
        token_service: TokenService,
        find_case: FindUserCase,
        update_case: UpdateUserCase,
    ):
        self.pwd_service = pwd_service
        self.token_sevice = token_service
        self.find_user_case = find_case
        self.update_user_case = update_case

    async def login(
        self,
        payload: JwtPayload,
    ) -> LoginResponse:
        hash_pass = self.pwd_service.hash_password(payload.password)

        user: User = self.find_user_case.get_user_by_username(payload["username"])

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

        token = self.token_sevice.generate_token(jwtPayload)

        await self.update_user_case.update_last_used(user.id)

        return {
            "acces_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
        }