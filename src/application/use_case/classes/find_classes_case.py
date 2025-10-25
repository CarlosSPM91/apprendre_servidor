from typing import List, Optional
from fastapi import HTTPException, status
from src.domain.objects.classes.class_subjects_dto import ClassSubjectsDTO
from src.infrastructure.entities.course.classes import Classes
from src.infrastructure.repositories.classes import ClassesRepository



class FindClassesCase:

    def __init__(self, repo: ClassesRepository):
        self.repo = repo

    async def get(self, class_id: int) -> Optional[ClassSubjectsDTO]:
        classes = await self.repo.get_by_id(class_id)
        if classes is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Class not found"
            )
        return classes

    async def get_all(self) -> List[Classes]:
        return await self.repo.get_all()
    