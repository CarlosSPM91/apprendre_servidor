
from typing import List, Optional
from pydantic import BaseModel

from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance
from src.infrastructure.entities.student_info.medical_info import MedicalInfo


class StudentUpdateDTO(BaseModel):
    student_id: int
    observations:Optional[str] = None
    medical_info: Optional[List[int]] = []
    allergies: Optional[List[int]] = []
    food_intolerance: Optional[List[int]] = [] 