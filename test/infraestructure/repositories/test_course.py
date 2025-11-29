from sqlite3 import IntegrityError
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException
import pytest

from src.infrastructure.entities.course.course import Course
from src.infrastructure.repositories.course import CourseRepository



@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def course_repository(mock_session):
    async def session_gen():
        yield mock_session
    return CourseRepository(session=session_gen)


@pytest.mark.asyncio
async def test_init():
    mock_session_test = MagicMock()
    course_repo = CourseRepository(mock_session_test)
    assert course_repo.session == mock_session_test

@pytest.mark.asyncio
async def test_get_course_success(course_repository, mock_session):
    mock_exec_result = MagicMock() 
    mock_exec_result.first.return_value = Course(
        id=1,
        year=2025,
    )
    mock_session.exec = AsyncMock(return_value=mock_exec_result) 

    result = await course_repository.get(1)  

    assert result.id == 1
    assert result.year == 2025
    mock_session.exec.assert_awaited_once() 

@pytest.mark.asyncio
async def test_create_course_success(course_repository, mock_session):
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    new_course = Course(
        year= 2025,
    )

    result = await course_repository.create(new_course)

    assert result.year == 2025
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_course_success(course_repository, mock_session):
    existing_course = Course(
        year= 2025,
    )

    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = existing_course
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    updated_course = Course(
        id=1,
        year= 2026,
    )

    result = await course_repository.update(updated_course)

    assert result.year == 2026
    mock_session.exec.assert_awaited_once()
    mock_session.commit.assert_awaited_once() 
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_course_not_found(course_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = None
    mock_session.exec = AsyncMock(return_value=mock_exec_result)

    non_existent_course = Course(
        id=999,
        year=2026,
    )

    with pytest.raises(Exception) as exc_info:
        await course_repository.update(non_existent_course)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Course not found"
    mock_session.exec.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_course_success(course_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    await course_repository.delete(1)

    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_awaited_once()
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_course_not_found(course_repository, mock_session):
    mock_result_select = MagicMock()
    mock_result_select.first = MagicMock(return_value=None)
    
    mock_session.exec = AsyncMock(return_value=mock_result_select)
    mock_session.delete = AsyncMock()

    with pytest.raises(HTTPException) as exc_info:
        await course_repository.delete(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Course not found"
    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()

@pytest.mark.asyncio
async def test_get_all_course_info_success(mock_session):
    fake_items = [Course(id=1), Course(id=2)]

    mock_exec_result = AsyncMock()
    mock_exec_result = MagicMock()
    mock_exec_result.all.return_value = fake_items
    mock_session.exec = AsyncMock(return_value=mock_exec_result)



    async def fake_session_gen():
        yield mock_session
    repo = CourseRepository(session=fake_session_gen)
    result = await repo.get_all()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2
    mock_session.exec.assert_awaited_once()
