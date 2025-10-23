from typing import List, Optional
from pydantic import BaseModel

from src.domain.objects.subject_dto import SubjectDTO


class TeacherUpdateDTO(BaseModel):
    teacher_id:int
    subjects:Optional[List[int]] = []