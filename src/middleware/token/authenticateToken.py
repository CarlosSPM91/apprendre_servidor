from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dependency_injector.wiring import inject, Provide
from src.application.services.token_service import TokenService
from src.container import Container
from src.domain.objects.token.jwtPayload import JwtPayload


secutiry = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(secutiry),
    token_service: TokenService = Depends(Provide[Container.token_service]),
) -> JwtPayload:
    token = credentials.credentials
    return await token_service.validate_token(token)

async def get_token(
    credentials: HTTPAuthorizationCredentials = Depends(secutiry),
) -> str:
    return credentials.credentials


def require_role(required_roles: int):
    
    async def role_checker(
      credentials: HTTPAuthorizationCredentials = Depends(secutiry),
        token_service: TokenService = Depends(Provide[Container.token_service]),
    ) -> JwtPayload:
        token= credentials.credentials
        user_payload= await token_service.validate_token(token)
        if user_payload.role not in required_roles:
            roles_str = ", ".join(map(str, required_roles))
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Requires one of these roles: {roles_str}"
            )
        
        return user_payload
    return role_checker
