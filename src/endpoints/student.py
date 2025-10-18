
from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.profiles.student_update_dto import StudentUpdateDTO
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.student import StudentController
from src.infrastructure.entities.student_info.student import Student
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/student", tags=["student"])

@router.get(
    "/{student_id}/find",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of student",
    response_description="Returns the information of student",
)
@inject
async def find(
    student_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentController = Depends(Provide[Container.student_contoller]),
):
    return await controller.get_student_full_info(student_id=student_id)

@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create the student base",
    response_description="Returns the information of student",
)
@inject
async def create(
    user_id:int = Body(..., embed=True),
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentController = Depends(Provide[Container.student_contoller]),
):
    return await controller.create(user_id=user_id)

@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-student",
    summary="Update an existing student",
    response_description="Returns the updated student information",
)
@inject
async def update_user(
    payload: StudentUpdateDTO,
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentController = Depends(Provide[Container.student_contoller]),
):
    return await controller.update(payload)

@router.delete(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    name="delete-user",
    summary="Delete a user",
    response_description="Returns the deleted user ID and timestamp",
)
@inject
async def delete_student(
    student_id: int,
    controller: StudentController = Depends(Provide[Container.student_contoller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    return await controller.delete(student_id=student_id)