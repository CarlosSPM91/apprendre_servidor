from typing import List, Optional
from fastapi import HTTPException, status
from src.domain.objects.profiles.teacher_dto import TeacherDTO
from src.infrastructure.entities.users.teacher import Teacher
from src.infrastructure.repositories.teacher import TeacherRepository



class FindTeacherCase:

    def __init__(self, repo: TeacherRepository):
        self.repo = repo

    async def get(self, student_id: int) -> Optional[Teacher]:
        teacher = await self.repo.get_teacher(student_id)
        if teacher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found"
            )
        return teacher
    
    async def get_all(self) -> Optional[TeacherDTO]:
        student = await self.repo.get_all()
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found"
            )
        return student


    async def get_teacher_full_info(self, teacher_id: int) -> Optional[TeacherDTO]:
        teacher: Optional[TeacherDTO] = await self.repo.get_teacher_full_info(
            teacher_id=teacher_id
        )
        if teacher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found"
            )
        return teacher
