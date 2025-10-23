
from typing import List, Optional
from pydantic import BaseModel

from src.domain.objects.subject_dto import SubjectDTO


class TeacherDTO(BaseModel):
    user_id:int
    teacher_id:int
    username: str
    name: str
    last_name: str
    email: Optional[str]= ""
    phone: Optional[int] = 0
    dni: Optional[str] = ""
    subjects:Optional[List[SubjectDTO]] = []
