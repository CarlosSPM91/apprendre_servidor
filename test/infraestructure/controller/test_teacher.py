import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from datetime import datetime, timezone

from src.infrastructure.controllers.teacher import TeacherController


@pytest.fixture
def create_case():
    return AsyncMock()


@pytest.fixture
def delete_case():
    return AsyncMock()


@pytest.fixture
def find_case():
    return AsyncMock()


@pytest.fixture
def teacher_controller(find_case, create_case, delete_case):
    return TeacherController(
        find_case=find_case,
        create_case=create_case,
        delete_case=delete_case,
    )


@pytest.mark.asyncio
async def test_create_teacher_success(teacher_controller, create_case):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)
    create_case.create.return_value = mock_response

    response = await teacher_controller.create(1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "deleted_date" in response["data"]
    create_case.create.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_create_teacher_exception(teacher_controller, create_case):
    create_case.create.side_effect = HTTPException(status_code=400, detail="Error creating teacher")

    with pytest.raises(HTTPException):
        await teacher_controller.create(1)
    create_case.create.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_delete_teacher_success(teacher_controller, delete_case):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)
    delete_case.delete.return_value = mock_response

    response = await teacher_controller.delete(teacher_id=1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "deleted_date" in response["data"]
    delete_case.delete.assert_awaited_once_with(teacher_id=1)


@pytest.mark.asyncio
async def test_delete_teacher_exception(teacher_controller, delete_case):
    delete_case.delete.side_effect = HTTPException(status_code=404, detail="Teacher not found")

    with pytest.raises(HTTPException):
        await teacher_controller.delete(teacher_id=1)
    delete_case.delete.assert_awaited_once_with(teacher_id=1)


@pytest.mark.asyncio
async def test_get_teacher_success(teacher_controller, find_case):
    mock_teacher = MagicMock()
    find_case.get_teacher_full_info.return_value = mock_teacher

    response = await teacher_controller.get(teacher_id=1)

    assert response["status"] == "success"
    assert response["data"] == mock_teacher
    find_case.get_teacher_full_info.assert_awaited_once_with(teacher_id=1)


@pytest.mark.asyncio
async def test_get_teacher_exception(teacher_controller, find_case):
    find_case.get_teacher_full_info.side_effect = HTTPException(status_code=404, detail="Teacher not found")

    with pytest.raises(HTTPException):
        await teacher_controller.get(teacher_id=1)
    find_case.get_teacher_full_info.assert_awaited_once_with(teacher_id=1)


@pytest.mark.asyncio
async def test_get_all_teachers_success(teacher_controller, find_case):
    mock_teachers = [MagicMock(), MagicMock()]
    find_case.get_all.return_value = mock_teachers

    response = await teacher_controller.get_all()

    assert response["status"] == "success"
    assert response["data"] == mock_teachers
    find_case.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_teachers_exception(teacher_controller, find_case):
    find_case.get_all.side_effect = HTTPException(status_code=500, detail="Server error")

    with pytest.raises(HTTPException):
        await teacher_controller.get_all()
    find_case.get_all.assert_awaited_once()
