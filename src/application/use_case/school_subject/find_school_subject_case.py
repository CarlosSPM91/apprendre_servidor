from typing import List, Optional
from fastapi import HTTPException, status
from src.infrastructure.entities.course.course import Course
from src.infrastructure.entities.course.school_subject import SchoolSubject
from src.infrastructure.repositories.school_subject import SchoolSubjectRepository



class FindSchoolSubjectCase:

    def __init__(self, repo: SchoolSubjectRepository):
        self.repo = repo

    async def get(self, school_subject_id: int) -> Optional[SchoolSubject]:
        school_subject = await self.repo.get(school_subject_id)
        if school_subject is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="School Subject not found"
            )
        return school_subject

    async def get_all(self) -> List[SchoolSubject]:
        return await self.repo.get_all()