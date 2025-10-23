from typing import List, Optional
from pydantic import BaseModel

from src.domain.objects.profiles.student_info_dto import StudentInfoDTO


class ParentDTO(BaseModel):
    user_id:int
    name:str
    last_name:str
    email: Optional[str] = None
    phone: Optional[int] = None
    students: Optional[List[int]]=[]