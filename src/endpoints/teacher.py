from fastapi import APIRouter, Body, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.domain.objects.profiles.teacher_dto import TeacherDTO
from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.teacher import TeacherController
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find-all-teacher",
    summary="Get all teachers",
    response_description="Returns a list of teachers",
    )
@inject
async def find_all(
    current_user: JwtPayload = Depends(get_current_user),
    controller: TeacherController = Depends(Provide[Container.teacher_controller])
):
    return await controller.get_all()


@router.get(
    "/{teacher_id}",
    status_code=status.HTTP_200_OK,
    name="findTeacher",
    summary="Get one teacher",
    response_description="Returns information of a teacher",
    )
@inject
async def find(
    teacher_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: TeacherController = Depends(Provide[Container.teacher_controller])
):
    return await controller.get(teacher_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="deleteTeacher",
    summary="Delete one teacher",
    response_description="Delete one teacher"
    )
@inject
async def create(
    user_id: int = Body(..., embed=True),
    current_user: JwtPayload = Depends(get_current_user),
    controller: TeacherController = Depends(Provide[Container.teacher_controller])
):
    return await controller.create(user_id)

@router.delete(
    "/{teacher_id}",
    status_code=status.HTTP_200_OK,
    name="deleteTeacher",
    summary="Delete one teacher",
    response_description="Delete one teacher"
    )
@inject
async def delete(
    teacher_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: TeacherController = Depends(Provide[Container.teacher_controller])
):
    return await controller.delete(teacher_id)
