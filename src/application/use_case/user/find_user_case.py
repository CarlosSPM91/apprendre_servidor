from typing import List, Optional

from fastapi import HTTPException, status
from src.domain.objects.user.user_dto import UserDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.repositories.user import UserRepository


class FindUserCase:
    def __init__(self, repo: UserRepository):
        self.userRepo = repo

    async def get_user_by_username(self, user_id: int) -> Optional[UserUpdateDTO]:
        user = await self.userRepo.get_user_by_username(user_id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        user =  await self.userRepo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
    async def get_all(self, user_id: int) -> Optional[List[UserDTO]]:
        users: Optional[List[UserDTO]] =  await self.userRepo.get_all()
        if users is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
        return users