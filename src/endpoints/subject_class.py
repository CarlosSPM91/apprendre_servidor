from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.subject_class import SubjectClassController
from src.infrastructure.entities.course.school_subject import SchoolSubject
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/subject_classes", tags=["subject_classes"])


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of all subject class",
    response_description="Returns a list of all subject class",
)
@inject
async def find_all(
    controller: SubjectClassController = Depends(Provide[Container.subject_class_controller]),
):
    return await controller.get_all()


@router.get(
    "/{subject_class_id}",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of subject class",
    response_description="Returns the information of a subject class",
)
@inject
async def find(
    subject_class_id: int,
    current_user: JwtPayload = Depends(get_current_user),
    controller: SubjectClassController = Depends(Provide[Container.subject_class_controller]),
):
    return await controller.get(subject_class_id)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    name="create",
    summary="Create a subject class",
    response_description="Returns the information of a subject class",
)
@inject
async def create(
    payload: SchoolSubject,
    current_user: JwtPayload = Depends(get_current_user),
    controller: SubjectClassController = Depends(Provide[Container.subject_class_controller]),
):
    return await controller.create(payload)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    name="update",
    summary="Update an existing subject class",
    response_description="Returns the updated subject class",
)
@inject
async def update(
    payload: SchoolSubject,
    current_user: JwtPayload = Depends(get_current_user),
    controller: SubjectClassController = Depends(Provide[Container.subject_class_controller]),
):
    return await controller.update(payload)


@router.delete(
    "/{subject_class_id}",
    status_code=status.HTTP_200_OK,
    name="delete",
    summary="Delete a subject class",
    response_description="Returns the deleted subject class id",
)
@inject
async def delete(
    subject_class_id: int,
    controller: SubjectClassController = Depends(Provide[Container.subject_class_controller]),
    current_user: JwtPayload = Depends(get_current_user),
):
    return await controller.delete(subject_class_id)
