from typing import Callable
import jwt
import redis
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from src.settings import settings
from src.application.use_case.user.find_user_case import FindUserCase
from src.domain.objects.token.jwtPayload import JwtPayload


class TokenService:
    def __init__(self, find_case: FindUserCase, redis_session: Callable):
        self.jwt_secret = settings.secret_key
        self.jwt_algorithm = settings.algorithm
        self.jwt_expiration = 24
        self.find_case = find_case
        self.redis = redis_session

    async def generate_token(self, payload: JwtPayload) -> str:
        tokenPayload = payload.to_dict()
        token = jwt.encode(tokenPayload, self.jwt_secret, self.jwt_algorithm)
        try:
            await self.save_token(user_id=payload.user_id, token=token)
            return token
        except Exception as e:
            print(e)

    async def get_user_info(
        self,
        token: str,
    ):
        payload = self.decode_token(token=token)
        return JwtPayload.from_dict(payload)

    def decode_token(self, token: str):
        return jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])

    async def validate_token(self, token: dict) -> None:
        try:
            print(token)
            is_listed = await self.is_token_listed(int(token.get("user_id")))
            if not is_listed:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has invalidated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            exp_time = token.get("exp")
            if exp_time and datetime.fromtimestamp(
                exp_time, tz=timezone.utc
            ) < datetime.now(timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def refresh_token(
        self,
        token: str,
    ) -> str:
        token_data = await self.validate_token(token)
        user = await self.find_case.get_user_by_id(token_data.user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "error", "message": "User not found"},
            )

        jwtPayload = JwtPayload(
            user_id=str(user.user_id),
            username=user.username,
            name=user.name,
            last_name=user.last_name,
            role=user.role,
        )

        new_token = self.generate_token(jwtPayload)

        return {
            "access_token": new_token,
            "token_type": "bearer",
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role,
        }

    async def save_token(
        self,
        token: str,
        user_id: int,
    ) -> bool:
        async for redis in self.redis():
            ttl_sec = 60 * 60 * 24
            await redis.setex(name=f"usertoken:{user_id}", value=token, time=ttl_sec)
            return True

    async def is_token_listed(self, user_id: int) -> bool:
        async for redis in self.redis():
            result = await redis.get(f"usertoken:{user_id}")
            return result is not None

    async def invalidate_token(self, user_id: int) -> bool:
        async for redis in self.redis():
            result = await redis.set(f"usertoken:{user_id}", "", ex=1)
            return result is not None
