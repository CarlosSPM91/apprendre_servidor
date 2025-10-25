from typing import List
from pydantic import BaseModel
from src.domain.objects.classes.subject_assignment_dto import SubjectAssignmentDTO


class UpdateClassSubjectsDTO(BaseModel):
    class_id: int
    subjects: List[SubjectAssignmentDTO]