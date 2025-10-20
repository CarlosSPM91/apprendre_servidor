from fastapi import HTTPException, status
from src.application.use_case.student.find_student_case import FindStudentCase
from src.application.use_case.user.find_user_case import FindUserCase
from src.domain.objects.profiles.parent_info import ParentDTO
from src.infrastructure.repositories.parent import ParentRepository


class FindParentCase:
    def __init__(
        self,
        repo: ParentRepository,
        find_user: FindUserCase,
    ):
        self.repo = repo
        self.find_user = find_user

    async def get(self, user_id: int) -> ParentDTO:
        parent_info = await self.repo.get(user_id)
        if not parent_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent with id {user_id} not found",
            )
        user = await self.find_user.get_user_by_id(user_id)

        return ParentDTO(
            user_id=user.user_id,
            name= user.name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            students=[ parent.student_id for parent in parent_info],
        )
