import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from datetime import datetime, timezone

from src.domain.objects.classes.subject_assignment_dto import SubjectAssignmentDTO
from src.infrastructure.controllers.classes import ClassesController
from src.infrastructure.entities.course.classes import Classes
from src.domain.objects.classes.update_class_subjects_dto import UpdateClassSubjectsDTO


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
def classes():
    return Classes(
        id=1,
        name="Class A",
        course_id=1
    )


@pytest.fixture
def update_subjects_payload():
    return UpdateClassSubjectsDTO(
        class_id=1,
        subjects=[SubjectAssignmentDTO(subject_id=1, teacher_id=2), SubjectAssignmentDTO(subject_id=2, teacher_id=2)]
    )


@pytest.fixture
def classes_controller(find_case, create_case, update_case, delete_case):
    return ClassesController(
        find_case=find_case,
        create_case=create_case,
        update_case=update_case,
        delete_case=delete_case,
    )


@pytest.mark.asyncio
async def test_create_classes_success(classes_controller, create_case, classes):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)
    create_case.create.return_value = mock_response

    response = await classes_controller.create(classes)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "created_date" in response["data"]
    create_case.create.assert_awaited_once_with(classes)


@pytest.mark.asyncio
async def test_create_classes_exception(classes_controller, create_case, classes):
    create_case.create.side_effect = HTTPException(status_code=400, detail="Error")

    with pytest.raises(HTTPException):
        await classes_controller.create(classes)

    create_case.create.assert_awaited_once_with(classes)



@pytest.mark.asyncio
async def test_update_classes_success(classes_controller, find_case, update_case, classes):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get.return_value = classes
    update_case.update.return_value = mock_response

    response = await classes_controller.update(classes)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "updated_date" in response["data"]

    find_case.get.assert_awaited_once_with(classes.id)
    update_case.update.assert_awaited_once_with(classes)


@pytest.mark.asyncio
async def test_update_classes_exception(classes_controller, find_case, update_case, classes):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await classes_controller.update(classes)

    find_case.get.assert_awaited_once_with(classes.id)
    update_case.update.assert_not_awaited()



@pytest.mark.asyncio
async def test_update_classes_subjects_success(
    classes_controller, find_case, update_case, update_subjects_payload
):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get = AsyncMock(return_value=MagicMock(id=1))
    update_case.update_subjects = AsyncMock(return_value=mock_response)

    response = await classes_controller.update_subjects(update_subjects_payload)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "updated_date" in response["data"]

    find_case.get.assert_awaited_once_with(update_subjects_payload.class_id)
    update_case.update_subjects.assert_awaited_once_with(update_subjects_payload)


@pytest.mark.asyncio
async def test_update_classes_subjects_exception(
    classes_controller, find_case, update_case, update_subjects_payload
):
    find_case.get = AsyncMock(side_effect=HTTPException(status_code=404, detail="Not found"))

    with pytest.raises(HTTPException):
        await classes_controller.update_subjects(update_subjects_payload)

    find_case.get.assert_awaited_once_with(update_subjects_payload.class_id)
    update_case.update_subjects.assert_not_awaited()




@pytest.mark.asyncio
async def test_delete_classes_success(classes_controller, find_case, delete_case):
    mock_response = MagicMock()
    mock_response.item_id = 1
    mock_response.event_date = datetime.now(timezone.utc)

    find_case.get.return_value = MagicMock(id=1)
    delete_case.delete.return_value = mock_response

    response = await classes_controller.delete(1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_response.item_id)
    assert "deletion_date" in response["data"]

    find_case.get.assert_awaited_once_with(1)
    delete_case.delete.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_delete_classes_exception(classes_controller, find_case, delete_case):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await classes_controller.delete(1)

    find_case.get.assert_awaited_once_with(1)
    delete_case.delete.assert_not_awaited()



@pytest.mark.asyncio
async def test_get_classes_success(classes_controller, find_case, classes):
    find_case.get.return_value = classes

    response = await classes_controller.get(classes_id="1")

    assert response["status"] == "success"
    assert response["data"] == classes
    find_case.get.assert_awaited_once_with("1")


@pytest.mark.asyncio
async def test_get_classes_exception(classes_controller, find_case):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await classes_controller.get(classes_id="999")

    find_case.get.assert_awaited_once_with("999")



@pytest.mark.asyncio
async def test_get_all_classes_success(classes_controller, find_case):
    fake_class = MagicMock()
    find_case.get_all.return_value = [fake_class]

    response = await classes_controller.get_all()

    assert response["status"] == "success"
    assert len(response["data"]) == 1

    find_case.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_classes_exception(classes_controller, find_case):
    find_case.get_all.side_effect = HTTPException(status_code=404, detail="Not found")

    with pytest.raises(HTTPException):
        await classes_controller.get_all()

    find_case.get_all.assert_awaited_once()
