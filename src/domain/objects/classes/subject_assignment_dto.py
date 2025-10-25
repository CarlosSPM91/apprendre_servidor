from pydantic import BaseModel


class SubjectAssignmentDTO(BaseModel):
    teacher_id: int
    subject_id: int