from typing import List, Optional
from fastapi import HTTPException, status
from src.infrastructure.entities.course.subject_class import SubjectClass
from src.infrastructure.repositories.subject_class import SubjectClassRepository



class FindSubjectClassCase:

    def __init__(self, repo: SubjectClassRepository):
        self.repo = repo

    async def get(self, student_class_id: int) -> Optional[SubjectClass]:
        subject_class = await self.repo.get(student_class_id)
        if subject_class is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Subject Class not found"
            )
        return student_class_id

    async def get_all(self) -> List[SubjectClass]:
        return await self.repo.get_all()