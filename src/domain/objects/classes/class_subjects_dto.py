
from typing import List, Optional
from pydantic import BaseModel


class ClassSubjectsDTO(BaseModel):
    id: int
    course_id: int 
    name: Optional[str] = None
    tutor_id: Optional[int]
    subjects: List[int]