

from typing import Optional
from pydantic import BaseModel


class SubjectDTO(BaseModel):
    subject_id: int
    subject_name:str
    description: Optional[str] = ""
    subject_class: Optional[int] = ""