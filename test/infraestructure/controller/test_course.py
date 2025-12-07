import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from datetime import datetime, timezone

from src.infrastructure.controllers.course import CourseController
from src.infrastructure.entities.course.course import Course


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
def course():
    return Course(
        id=1,
        name="Math",
        description="Basic math course"
    )


@pytest.fixture
def course_controller(find_case, create_case, update_case, delete_case):
    return CourseController(
        find_case=find_case,
        create_case=create_case,
        update_case=update_case,
        delete_case=delete_case,
    )


@pytest.mark.asyncio
async def test_create_course_success(course_controller, create_case, course):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)
    create_case.create.return_value = mock_response

    response = await course_controller.create(course)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "created_date" in response["data"]
    create_case.create.assert_awaited_once_with(course)


@pytest.mark.asyncio
async def test_create_course_exception(course_controller, create_case, course):
    create_case.create.side_effect = HTTPException(status_code=400, detail="Error")

    with pytest.raises(HTTPException):
        await course_controller.create(course)

    create_case.create.assert_awaited_once_with(course)



@pytest.mark.asyncio
async def test_update_course_success(course_controller, find_case, update_case, course):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get.return_value = course
    update_case.update.return_value = mock_response

    response = await course_controller.update(course)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "updated_date" in response["data"]

    find_case.get.assert_awaited_once_with(course.id)
    update_case.update.assert_awaited_once_with(course)


@pytest.mark.asyncio
async def test_update_course_exception(course_controller, find_case, update_case, course):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await course_controller.update(course)

    find_case.get.assert_awaited_once_with(course.id)
    update_case.update.assert_not_awaited()



@pytest.mark.asyncio
async def test_delete_course_success(course_controller, find_case, delete_case):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get.return_value = MagicMock(id=1)
    delete_case.delete.return_value = mock_response

    response = await course_controller.delete(1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "deletion_date" in response["data"]

    find_case.get.assert_awaited_once_with(1)
    delete_case.delete.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_delete_course_exception(course_controller, find_case, delete_case):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await course_controller.delete(1)

    find_case.get.assert_awaited_once_with(1)
    delete_case.delete.assert_not_awaited()



@pytest.mark.asyncio
async def test_get_course_success(course_controller, find_case, course):
    find_case.get.return_value = course

    response = await course_controller.get(course_id="1")

    assert response["status"] == "success"
    assert response["data"] == course
    find_case.get.assert_awaited_once_with("1")


@pytest.mark.asyncio
async def test_get_course_exception(course_controller, find_case):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await course_controller.get(course_id="999")

    find_case.get.assert_awaited_once_with("999")


@pytest.mark.asyncio
async def test_get_all_courses_success(course_controller, find_case):
    fake_course = MagicMock()
    find_case.get_all.return_value = [fake_course]

    response = await course_controller.get_all()

    assert response["status"] == "success"
    assert len(response["data"]) == 1

    find_case.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_courses_exception(course_controller, find_case):
    find_case.get_all.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await course_controller.get_all()

    find_case.get_all.assert_awaited_once()
