import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from datetime import datetime, timezone

from src.infrastructure.controllers.school_subject import SchoolSubjectController
from src.infrastructure.entities.course.school_subject import SchoolSubject


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
def school_subject_dto():
    return SchoolSubject(
        id=1,
        name="Math",
        description="Mathematics Subject",
    )

@pytest.fixture
def school_subject_controller(find_case, create_case, update_case, delete_case):
    return SchoolSubjectController(
        find_case=find_case,
        create_case=create_case,
        update_case=update_case,
        delete_case=delete_case,
    )



@pytest.mark.asyncio
async def test_create_school_subject_success(
    school_subject_controller, create_case, school_subject_dto
):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    create_case.create.return_value = mock_response

    response = await school_subject_controller.create(school_subject_dto)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "created_date" in response["data"]
    create_case.create.assert_awaited_once_with(school_subject_dto)


@pytest.mark.asyncio
async def test_update_school_subject_success(
    school_subject_controller, update_case, find_case, school_subject_dto
):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get.return_value = MagicMock(id=1)
    update_case.update.return_value = mock_response

    response = await school_subject_controller.update(school_subject_dto)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "updated_date" in response["data"]
    find_case.get.assert_awaited_once_with(school_subject_dto.id)
    update_case.update.assert_awaited_once_with(school_subject_dto)


@pytest.mark.asyncio
async def test_delete_school_subject_success(
    school_subject_controller, delete_case, find_case
):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get.return_value = MagicMock(id=1)
    delete_case.delete.return_value = mock_response

    response = await school_subject_controller.delete(school_subject_id=1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "deletion_date" in response["data"]
    find_case.get.assert_awaited_once_with(1)
    delete_case.delete.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_school_subject_success(
    school_subject_controller, find_case, school_subject_dto
):
    find_case.get.return_value = school_subject_dto

    response = await school_subject_controller.get(school_subject_id="1")

    assert response["status"] == "success"
    assert response["data"] == school_subject_dto
    find_case.get.assert_awaited_once_with("1")


@pytest.mark.asyncio
async def test_get_all_school_subject_success(
    school_subject_controller, find_case, school_subject_dto
):
    find_case.get_all.return_value = [school_subject_dto]

    response = await school_subject_controller.get_all()

    assert response["status"] == "success"
    assert len(response["data"]) == 1
    assert response["data"][0].id == school_subject_dto.id
    find_case.get_all.assert_awaited_once()

@pytest.mark.asyncio
async def test_create_school_subject_exception(
    school_subject_controller, create_case, school_subject_dto
):
    create_case.create.side_effect = HTTPException(status_code=400, detail="Error")

    with pytest.raises(HTTPException):
        await school_subject_controller.create(school_subject_dto)
    create_case.create.assert_awaited_once_with(school_subject_dto)


@pytest.mark.asyncio
async def test_update_school_subject_exception(
    school_subject_controller, find_case, update_case, school_subject_dto
):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await school_subject_controller.update(school_subject_dto)

    find_case.get.assert_awaited_once_with(school_subject_dto.id)
    update_case.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_school_subject_exception(
    school_subject_controller, find_case, delete_case
):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await school_subject_controller.delete(school_subject_id=999)

    find_case.get.assert_awaited_once_with(999)
    delete_case.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_school_subject_exception(
    school_subject_controller, find_case
):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await school_subject_controller.get(school_subject_id="999")

    find_case.get.assert_awaited_once_with("999")


@pytest.mark.asyncio
async def test_get_all_school_subject_exception(
    school_subject_controller, find_case
):
    find_case.get_all.side_effect = HTTPException(status_code=500, detail="Error")

    with pytest.raises(HTTPException):
        await school_subject_controller.get_all()

    find_case.get_all.assert_awaited_once()
