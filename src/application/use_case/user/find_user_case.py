from typing import Optional

from fastapi import HTTPException, status
from src.domain.objects.user.user_dto import UserDTO
from src.infrastructure.entities.user import User
from src.infrastructure.repositories.user import UserRepository


class FindUserCase:
    def __init__(self, repo: UserRepository):
        self.userRepo = repo

    async def get_user_by_username(self, user_id: int) -> Optional[User]:
        user = self.userRepo.get_user_by_username(user_id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        user =  self.userRepo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user