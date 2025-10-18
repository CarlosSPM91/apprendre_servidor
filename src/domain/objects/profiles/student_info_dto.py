
from typing import List, Optional
from pydantic import BaseModel

from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance
from src.infrastructure.entities.student_info.medical_info import MedicalInfo


class StudentInfoDTO(BaseModel):
    student_id: int
    user_id:int
    name:str
    last_name:str
    email: Optional[str] = None
    phone: Optional[str] = None
    classe: Optional[str] = None
    obvervations:Optional[str] = None
    medical_info: Optional[List[MedicalInfo]] = []
    allergies: Optional[List[AllergyInfo]] = []
    food_intolerance: Optional[List[FoodIntolerance]] = [] 