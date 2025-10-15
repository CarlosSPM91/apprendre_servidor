from typing import List, Optional
from pydantic import BaseModel

from src.domain.objects.profiles.student_info_dto import StudentInfoDTO


class ParentDTO(BaseModel):
    students: Optional[List[StudentInfoDTO]]