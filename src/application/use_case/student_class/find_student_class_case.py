from typing import List, Optional
from fastapi import HTTPException, status
from src.infrastructure.entities.course.student_class import StudentClass
from src.infrastructure.repositories.student_class import StudentClassRepository



class FindStudentClassCase:

    def __init__(self, repo: StudentClassRepository):
        self.repo = repo

    async def get(self, student_class_id: int) -> Optional[StudentClass]:
        student_class = await self.repo.get(student_class_id)
        if student_class is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student Class not found"
            )
        return student_class

    async def get_all(self) -> List[StudentClass]:
        return await self.repo.get_all()