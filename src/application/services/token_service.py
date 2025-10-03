import jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from src import settings
from src.application.use_case.user.find_user_case import FindUserCase
from src.domain.objects.token.jwtPayload import JwtPayload


class TokenService:
    def __init__(self, find_case: FindUserCase):
        self.jwt_secret=settings.secret_key
        self.jwt_algorithm=settings.algorithm
        self.jwt_expiration=24
        self.find_case=find_case
    
    def generate_token(self, payload:JwtPayload) -> str:
        tokenPayload ={
            "id": payload.id,
            "username": payload.username,
            "name": payload.name,
            "last_name": payload.last_name,
            "role": payload.role,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc)+ timedelta(hours=self.jwt_expiration),
        }

        return jwt.encode(tokenPayload, self.jwt_secret, self.jwt_algorithm)
    
    async def validate_token(
            self,
            token:str,
    ):
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            exp_time = payload.get("exp")
            if exp_time and datetime.fromtimestamp(exp_time, tz=timezone.utc) < datetime.now(timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return {
                "valid": True,
                "user_id": payload.get("user_id"),
                "username": payload.get("username"),
                "role": payload.get("role"),
                "exprires_at": exp_time
            }
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
            token:str,
    ) -> str:
        token_data = self.validate_token(token)
        user = await self.find_case.get_user_by_id(int(token_data["user_id"]))

        if not user:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        
        jwtPayload = JwtPayload()
        jwtPayload.id = str(user.id)
        jwtPayload.username = user.username
        jwtPayload.name = user.name
        jwtPayload.last_name = user.last_name
        jwtPayload.role = user.role

        new_token = self.generate_token(jwtPayload)

        return {
            "acces_token": new_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
        }