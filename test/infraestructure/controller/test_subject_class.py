import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from datetime import datetime, timezone

from src.infrastructure.controllers.subject_class import SubjectClassController
from src.infrastructure.entities.course.subject_class import SubjectClass


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
def subject_class_dto():
    return SubjectClass(
        id=1,
        subject_id=1,
        class_id=1,
        teacher_id=1
    )

@pytest.fixture
def subject_class_controller(find_case, create_case, update_case, delete_case):
    return SubjectClassController(
        find_case=find_case,
        create_case=create_case,
        update_case=update_case,
        delete_case=delete_case,
    )

@pytest.mark.asyncio
async def test_create_subject_class_success(
    subject_class_controller, create_case, subject_class_dto
):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)
    create_case.create.return_value = mock_response

    response = await subject_class_controller.create(subject_class_dto)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "created_date" in response["data"]
    create_case.create.assert_awaited_once_with(subject_class_dto)


@pytest.mark.asyncio
async def test_update_subject_class_success(
    subject_class_controller, update_case, find_case, subject_class_dto
):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get.return_value = MagicMock(id=1)
    update_case.update.return_value = mock_response

    response = await subject_class_controller.update(subject_class_dto)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "updated_date" in response["data"]

    find_case.get.assert_awaited_once_with(subject_class_dto.id)
    update_case.update.assert_awaited_once_with(subject_class_dto)


@pytest.mark.asyncio
async def test_delete_subject_class_success(
    subject_class_controller, delete_case, find_case
):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get.return_value = MagicMock(id=1)
    delete_case.delete.return_value = mock_response

    response = await subject_class_controller.delete(subject_class_id=1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "deletion_date" in response["data"]

    find_case.get.assert_awaited_once_with(1)
    delete_case.delete.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_subject_class_success(
    subject_class_controller, find_case, subject_class_dto
):
    find_case.get.return_value = subject_class_dto

    response = await subject_class_controller.get(subject_class_id="1")

    assert response["status"] == "success"
    assert response["data"] == subject_class_dto
    find_case.get.assert_awaited_once_with("1")


@pytest.mark.asyncio
async def test_get_all_subject_class_success(
    subject_class_controller, find_case, subject_class_dto
):
    find_case.get_all.return_value = [subject_class_dto]

    response = await subject_class_controller.get_all()

    assert response["status"] == "success"
    assert len(response["data"]) == 1
    assert response["data"][0].id == subject_class_dto.id

    find_case.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_subject_class_exception(
    subject_class_controller, create_case, subject_class_dto
):
    create_case.create.side_effect = HTTPException(status_code=400, detail="Error")

    with pytest.raises(HTTPException):
        await subject_class_controller.create(subject_class_dto)

    create_case.create.assert_awaited_once_with(subject_class_dto)


@pytest.mark.asyncio
async def test_update_subject_class_exception(
    subject_class_controller, find_case, update_case, subject_class_dto
):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await subject_class_controller.update(subject_class_dto)

    find_case.get.assert_awaited_once_with(subject_class_dto.id)
    update_case.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_subject_class_exception(
    subject_class_controller, find_case, delete_case
):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await subject_class_controller.delete(subject_class_id=999)

    find_case.get.assert_awaited_once_with(999)
    delete_case.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_subject_class_exception(
    subject_class_controller, find_case
):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await subject_class_controller.get(subject_class_id="999")

    find_case.get.assert_awaited_once_with("999")


@pytest.mark.asyncio
async def test_get_all_subject_class_exception(
    subject_class_controller, find_case
):
    find_case.get_all.side_effect = HTTPException(status_code=500, detail="Error")

    with pytest.raises(HTTPException):
        await subject_class_controller.get_all()

    find_case.get_all.assert_awaited_once()
