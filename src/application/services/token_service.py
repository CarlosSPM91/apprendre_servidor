"""
Token Service.

Provides JWT token management, validation, refresh, and storage in Redis.

:author: Carlos S. Paredes Morillo
"""

from typing import Callable, Dict, Any
import jwt
import redis
from fastapi import HTTPException, status
from datetime import datetime, timezone
from src.settings import settings
from src.application.use_case.user.find_user_case import FindUserCase
from src.domain.objects.token.jwtPayload import JwtPayload


class TokenService:
    """Service for generating, validating, refreshing, and invalidating JWT tokens.

    Stores tokens in Redis and interacts with user data via FindUserCase.
    """

    def __init__(self, find_case: FindUserCase, redis_session: Callable):
        """
        Initialize the TokenService.

        Args:
            find_case (FindUserCase): Use case for retrieving user information.
            redis_session (Callable): Async Redis session factory.
        """
        self.jwt_secret = settings.secret_key
        self.jwt_algorithm = settings.algorithm
        self.jwt_expiration = 24
        self.find_case = find_case
        self.redis = redis_session

    async def generate_token(self, payload: JwtPayload) -> str:
        """
        Generate a JWT token for a user and save it in Redis.

        Args:
            payload (JwtPayload): The user payload to encode in the token.

        Returns:
            str: The generated JWT token.

        Raises:
            HTTPException: If token saving fails.
        """
        tokenPayload = payload.to_dict()
        token = jwt.encode(tokenPayload, self.jwt_secret, self.jwt_algorithm)
        try:
            await self.save_token(user_id=int(payload.user_id), token=token)
            return token
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def get_user_info(self, token: str) -> JwtPayload:
        """
        Decode a JWT token and return the corresponding user information.

        Args:
            token (str): The JWT token.

        Returns:
            JwtPayload: The decoded user payload.
        """
        payload = self.decode_token(token=token)
        return JwtPayload.from_dict(payload)

    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decode a JWT token.

        Args:
            token (str): The JWT token.

        Returns:
            dict: The decoded payload.
        """
        return jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])

    async def validate_token(self, token: Dict[str, Any]) -> None:
        """
        Validate a token by checking its existence in Redis and expiration.

        Args:
            token (dict): The token payload dictionary.

        Raises:
            HTTPException: If the token is expired or invalid.
        """
        try:
            is_listed = await self.is_token_listed(int(token.get("user_id")))
            if not is_listed:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has invalidated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            exp_time = token.get("exp")
            if exp_time and datetime.fromtimestamp(exp_time, tz=timezone.utc) < datetime.now(timezone.utc):
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
                detail="Token is invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def refresh_token(self, token: str) -> Dict[str, Any]:
        """
        Refresh a valid JWT token and return a new token with updated expiration.

        Args:
            token (str): The current JWT token.

        Returns:
            dict: Contains the new access token, token type, and user info.

        Raises:
            HTTPException: If the user is not found.
        """
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

        new_token = await self.generate_token(jwtPayload)

        return {
            "access_token": new_token,
            "token_type": "bearer",
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role,
        }

    async def save_token(self, token: str, user_id: int) -> bool:
        """
        Save a token in Redis with a TTL of 24 hours.

        Args:
            token (str): The JWT token to save.
            user_id (int): The user's ID.

        Returns:
            bool: True if successfully saved.
        """
        async for redis in self.redis():
            ttl_sec = 60 * 60 * 24
            await redis.setex(name=f"usertoken:{user_id}", value=token, time=ttl_sec)
            return True

    async def is_token_listed(self, user_id: int) -> bool:
        """
        Check if a token exists for the user in Redis.

        Args:
            user_id (int): The user's ID.

        Returns:
            bool: True if a token exists, False otherwise.
        """
        async for redis in self.redis():
            result = await redis.get(f"usertoken:{user_id}")
            return result is not None

    async def invalidate_token(self, user_id: int) -> bool:
        """
        Invalidate a user's token by setting a short expiry in Redis.

        Args:
            user_id (int): The user's ID.

        Returns:
            bool: True if successfully invalidated.
        """
        async for redis in self.redis():
            result = await redis.set(f"usertoken:{user_id}", "", ex=1)
            return result is not None
