from typing import List, Optional
from fastapi import HTTPException, status
from src.infrastructure.entities.course.course import Course
from src.infrastructure.repositories.course import CourseRepository



class FindCourseCase:

    def __init__(self, repo: CourseRepository):
        self.repo = repo

    async def get(self, intolerance_id: int) -> Optional[Course]:
        course = await self.repo.get(intolerance_id)
        if course is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
            )
        return course

    async def get_all(self) -> List[Course]:
        return await self.repo.get_all()