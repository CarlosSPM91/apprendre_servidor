import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from datetime import datetime, timezone

from src.infrastructure.controllers.student_class import StudentClassController
from src.infrastructure.entities.course.student_class import StudentClass

@pytest.fixture
def create_case():
    return AsyncMock()

@pytest.fixture
def update_case():
    return AsyncMock()

@pytest.fixture
def delete_case():
    return AsyncMock()

@pytest.fixture
def find_case():
    return AsyncMock()

@pytest.fixture
def student_class_dto():
    return StudentClass(
        id=1,
        student_id=1,
        class_id=1,
        points=10
    )

@pytest.fixture
def student_class_controller(find_case, create_case, update_case, delete_case):
    return StudentClassController(
        find_case=find_case,
        create_case=create_case,
        update_case=update_case,
        delete_case=delete_case,
    )

@pytest.mark.asyncio
async def test_create_student_class_success(
    student_class_controller, create_case, student_class_dto
):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    create_case.create.return_value = mock_response

    response = await student_class_controller.create(student_class_dto)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "created_date" in response["data"]

    create_case.create.assert_awaited_once_with(student_class_dto)


@pytest.mark.asyncio
async def test_update_student_class_points_success(
    student_class_controller, update_case, find_case, student_class_dto
):

    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get = AsyncMock(return_value=MagicMock(id=1))
    update_case.update_points = AsyncMock(return_value=mock_response)


    response = await student_class_controller.update_points(student_class_dto)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "updated_date" in response["data"]

    find_case.get.assert_awaited_once_with(student_class_dto.id)
    update_case.update_points.assert_awaited_once_with(student_class_dto)



@pytest.mark.asyncio
async def test_delete_student_class_success(
    student_class_controller, delete_case, find_case
):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get.return_value = MagicMock(id=1)
    delete_case.delete.return_value = mock_response

    response = await student_class_controller.delete(student_class_id=1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "deletion_date" in response["data"]

    find_case.get.assert_awaited_once_with(1)
    delete_case.delete.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_student_class_success(
    student_class_controller, find_case, student_class_dto
):
    find_case.get.return_value = student_class_dto

    response = await student_class_controller.get(student_class_id="1")

    assert response["status"] == "success"
    assert response["data"] == student_class_dto
    find_case.get.assert_awaited_once_with("1")


@pytest.mark.asyncio
async def test_get_all_student_class_success(
    student_class_controller, find_case, student_class_dto
):
    find_case.get_all.return_value = [student_class_dto]

    response = await student_class_controller.get_all()

    assert response["status"] == "success"
    assert len(response["data"]) == 1
    assert response["data"][0].id == student_class_dto.id

    find_case.get_all.assert_awaited_once()



@pytest.mark.asyncio
async def test_create_student_class_exception(
    student_class_controller, create_case, student_class_dto
):
    create_case.create.side_effect = HTTPException(status_code=400, detail="Error")

    with pytest.raises(HTTPException):
        await student_class_controller.create(student_class_dto)

    create_case.create.assert_awaited_once_with(student_class_dto)


@pytest.mark.asyncio
async def test_update_student_class_exception(
    student_class_controller, find_case, update_case, student_class_dto
):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await student_class_controller.update_points(student_class_dto)

    find_case.get.assert_awaited_once_with(student_class_dto.id)
    update_case.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_student_class_exception(
    student_class_controller, find_case, delete_case
):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await student_class_controller.delete(student_class_id=999)

    find_case.get.assert_awaited_once_with(999)
    delete_case.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_student_class_exception(
    student_class_controller, find_case
):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await student_class_controller.get(student_class_id="999")

    find_case.get.assert_awaited_once_with("999")


@pytest.mark.asyncio
async def test_get_all_student_class_exception(
    student_class_controller, find_case
):
    find_case.get_all.side_effect = HTTPException(status_code=500, detail="Error")

    with pytest.raises(HTTPException):
        await student_class_controller.get_all()

    find_case.get_all.assert_awaited_once()
