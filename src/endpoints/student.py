
from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from src.container import Container

from src.domain.objects.token.jwtPayload import JwtPayload
from src.infrastructure.controllers.student import StudentController
from src.middleware.token.authenticateToken import get_current_user


router = APIRouter(prefix="/student", tags=["student"])

@router.get(
    "/{id}/find",
    status_code=status.HTTP_200_OK,
    name="find",
    summary="Get information of student",
    response_description="Returns the information of student",
)
@inject
async def find(
    current_user: JwtPayload = Depends(get_current_user),
    controller: StudentController = Depends(Provide[Container.student_contoller]),
):
    return await controller.get_all()