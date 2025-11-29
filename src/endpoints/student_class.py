from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.student_class import StudentClassController
from src.infrastructure.entities.course.student_class import StudentClass
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/student_classes", tags=["student_classes"])


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of all student class",
    response_description="Returns a list of all student class",
)
@inject
async def find_all(
    controller: StudentClassController = Depends(Provide[Container.student_class_controller]),
):
    return await controller.get_all()


@router.get(
    "/{student_class_id}",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of student class",
    response_description="Returns the information of a student class",
)
@inject
async def find(
    student_class_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentClassController = Depends(Provide[Container.student_class_controller]),
):
    return await controller.get(student_class_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create a student class",
    response_description="Returns the information of a student class",
)
@inject
async def create(
    payload: StudentClass,
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentClassController = Depends(Provide[Container.student_class_controller]),
):
    return await controller.create(payload)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update-points",
    summary="Update points of student ",
    response_description="Returns the updated student class",
)
@inject
async def update(
    payload: StudentClass,
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentClassController = Depends(Provide[Container.student_class_controller]),
):
    return await controller.update_points(payload)


@router.delete(
    "/{student_class_id}",
    status_code=status.HTTP_200_OK,
    name="delete",
    summary="Delete a student class",
    response_description="Returns the deleted student class id",
)
@inject
async def delete(
    student_class_id: int,
    controller: StudentClassController = Depends(Provide[Container.student_class_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    return await controller.delete(student_class_id)
