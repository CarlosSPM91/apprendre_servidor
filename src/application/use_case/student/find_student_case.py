from typing import List, Optional
from fastapi import HTTPException, status
from src.domain.objects.profiles.student_info_dto import StudentInfoDTO
from src.domain.objects.user.user_dto import UserDTO
from src.infrastructure.entities.student_info.student import Student
from src.infrastructure.repositories.student import StudentRepository



class FindStudentCase:

    def __init__(self, repo: StudentRepository):
        self.repo = repo

    async def get_student_by_id(self, student_id: int) -> Optional[UserDTO]:
        student = await self.repo.get_student(student_id)
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
            )
        return student
    
    async def get_all(self) -> List[Student]:
        return await self.repo.get_all()

    async def get_student_full_info(self, student_id: int) -> Optional[StudentInfoDTO]:
        student: Optional[StudentInfoDTO] = await self.repo.get_student_full_info(
            student_id=student_id
        )
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
            )
        return student
