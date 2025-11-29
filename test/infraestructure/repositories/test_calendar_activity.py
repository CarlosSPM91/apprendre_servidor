import datetime
from sqlite3 import IntegrityError
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException
import pytest

from src.infrastructure.entities.course.calendary_activity import CalendarActivity
from src.infrastructure.repositories.calendary_activity import CalendarActivityRepository




@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def calendar_activity_repository(mock_session):
    async def session_gen():
        yield mock_session
    return CalendarActivityRepository(session=session_gen)


@pytest.mark.asyncio
async def test_init():
    mock_session_test = MagicMock()
    calendar_activity_repo = CalendarActivityRepository(mock_session_test)
    assert calendar_activity_repo.session == mock_session_test

@pytest.mark.asyncio
async def test_get_calendar_activity_success(calendar_activity_repository, mock_session):
    mock_exec_result = MagicMock() 
    mock_exec_result.first.return_value = CalendarActivity(
        id=1,
        course_id=1,
        date= datetime.date.fromisoformat("2025-12-01"),
        activity_name="Exam"
    )
    mock_session.exec = AsyncMock(return_value=mock_exec_result) 

    result = await calendar_activity_repository.get(1)  

    assert result.id == 1
    assert result.course_id == 1
    assert result.date == datetime.date.fromisoformat("2025-12-01")
    assert result.activity_name == "Exam"
    mock_session.exec.assert_awaited_once() 

@pytest.mark.asyncio
async def test_create_calendar_activity_success(calendar_activity_repository, mock_session):
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    new_calendar_activity = CalendarActivity(
        course_id=1,
        date= datetime.date.fromisoformat("2025-12-01"),
        activity_name="Exam"
    )

    result = await calendar_activity_repository.create(new_calendar_activity)

    assert result.date == datetime.date.fromisoformat("2025-12-01")
    assert result.activity_name == "Exam"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_calendar_activity_success(calendar_activity_repository, mock_session):
    existing_calendar_activity = CalendarActivity(
        id=1,
        course_id=1,
        date= datetime.date.fromisoformat("2025-12-01"),
        activity_name="Exam"
    )

    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = existing_calendar_activity
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    updated_calendar_activity = CalendarActivity(
        id=1,
        course_id=1,
        date= datetime.date.fromisoformat("2025-12-15"),
        activity_name="Math Exam"
    )

    result = await calendar_activity_repository.update(updated_calendar_activity)

    assert result.date == datetime.date.fromisoformat("2025-12-15")
    assert result.activity_name == "Math Exam"
    mock_session.exec.assert_awaited_once()
    mock_session.commit.assert_awaited_once() 
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_calendar_activity_not_found(calendar_activity_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = None
    mock_session.exec = AsyncMock(return_value=mock_exec_result)

    non_existent_calendar_activity = CalendarActivity(
        id=1,
        course_id=1,
        date= datetime.date.fromisoformat("2025-12-01"),
        activity_name="Exam"
    )

    with pytest.raises(Exception) as exc_info:
        await calendar_activity_repository.update(non_existent_calendar_activity)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Calendar Activity not found"
    mock_session.exec.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_calendar_activity_success(calendar_activity_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    await calendar_activity_repository.delete(1)

    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_awaited_once()
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_calendar_activity_not_found(calendar_activity_repository, mock_session):
    mock_result_select = MagicMock()
    mock_result_select.first = MagicMock(return_value=None)
    
    mock_session.exec = AsyncMock(return_value=mock_result_select)
    mock_session.delete = AsyncMock()

    with pytest.raises(HTTPException) as exc_info:
        await calendar_activity_repository.delete(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Calendar Activity not found"
    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()

@pytest.mark.asyncio
async def test_get_all_calendar_activity_info_success(mock_session):
    fake_items = [CalendarActivity(id=1), CalendarActivity(id=2)]

    mock_exec_result = AsyncMock()
    mock_exec_result = MagicMock()
    mock_exec_result.all.return_value = fake_items
    mock_session.exec = AsyncMock(return_value=mock_exec_result)



    async def fake_session_gen():
        yield mock_session
    repo = CalendarActivityRepository(session=fake_session_gen)
    result = await repo.get_all()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2
    mock_session.exec.assert_awaited_once()
