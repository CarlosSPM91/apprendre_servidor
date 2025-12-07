import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from datetime import datetime, timezone

from src.infrastructure.controllers.calendar_activity import CalendarController
from src.infrastructure.entities.course.calendary_activity import CalendarActivity



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
def calendar_activity_dto():
    return CalendarActivity(
        id=1,
        course_id=101,
        date=datetime(2025, 12, 15, 10, 0, tzinfo=timezone.utc),
        activity_name="Algebra Lesson",
        activity_type_id=5
    )

@pytest.fixture
def calendar_controller(find_case, create_case, update_case, delete_case):
    return CalendarController(
        find_case=find_case,
        create_case=create_case,
        update_case=update_case,
        delete_case=delete_case,
    )



@pytest.mark.asyncio
async def test_create_calendar_success(calendar_controller, create_case, calendar_activity_dto):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    create_case.create.return_value = mock_response

    response = await calendar_controller.create(calendar_activity_dto)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "created_date" in response["data"]
    create_case.create.assert_awaited_once_with(calendar_activity_dto)


@pytest.mark.asyncio
async def test_update_calendar_success(calendar_controller, update_case, find_case, calendar_activity_dto):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get.return_value = MagicMock(id=1)
    update_case.update.return_value = mock_response

    response = await calendar_controller.update(calendar_activity_dto)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "updated_date" in response["data"]
    find_case.get.assert_awaited_once_with(calendar_activity_dto.id)
    update_case.update.assert_awaited_once_with(calendar_activity_dto)


@pytest.mark.asyncio
async def test_delete_calendar_success(calendar_controller, delete_case, find_case):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get.return_value = MagicMock(id=1)
    delete_case.delete.return_value = mock_response

    response = await calendar_controller.delete(calendar_activity_id=1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "deletion_date" in response["data"]
    find_case.get.assert_awaited_once_with(1)
    delete_case.delete.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_calendar_success(calendar_controller, find_case, calendar_activity_dto):
    find_case.get.return_value = calendar_activity_dto

    response = await calendar_controller.get(calendar_activity_id="1")

    assert response["status"] == "success"
    assert response["data"] == calendar_activity_dto
    find_case.get.assert_awaited_once_with("1")


@pytest.mark.asyncio
async def test_get_all_calendar_success(calendar_controller, find_case, calendar_activity_dto):
    find_case.get_all.return_value = [calendar_activity_dto]

    response = await calendar_controller.get_all()

    assert response["status"] == "success"
    assert len(response["data"]) == 1
    assert response["data"][0].id == calendar_activity_dto.id
    find_case.get_all.assert_awaited_once()



@pytest.mark.asyncio
async def test_create_calendar_exception(calendar_controller, create_case, calendar_activity_dto):
    create_case.create.side_effect = HTTPException(status_code=400, detail="Error creating")

    with pytest.raises(HTTPException):
        await calendar_controller.create(calendar_activity_dto)
    create_case.create.assert_awaited_once_with(calendar_activity_dto)


@pytest.mark.asyncio
async def test_update_calendar_exception(calendar_controller, find_case, update_case, calendar_activity_dto):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await calendar_controller.update(calendar_activity_dto)

    find_case.get.assert_awaited_once_with(calendar_activity_dto.id)
    update_case.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_calendar_exception(calendar_controller, find_case, delete_case):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await calendar_controller.delete(calendar_activity_id=999)

    find_case.get.assert_awaited_once_with(999)
    delete_case.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_calendar_exception(calendar_controller, find_case):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await calendar_controller.get(calendar_activity_id="999")

    find_case.get.assert_awaited_once_with("999")


@pytest.mark.asyncio
async def test_get_all_calendar_exception(calendar_controller, find_case):
    find_case.get_all.side_effect = HTTPException(status_code=500, detail="Error")

    with pytest.raises(HTTPException):
        await calendar_controller.get_all()

    find_case.get_all.assert_awaited_once()
