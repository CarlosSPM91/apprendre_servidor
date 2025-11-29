from sqlite3 import IntegrityError
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException
import pytest

from src.infrastructure.entities.course.student_class import StudentClass
from src.infrastructure.repositories.student_class import StudentClassRepository


@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def studentClass_repository(mock_session):
    async def session_gen():
        yield mock_session
    return StudentClassRepository(session=session_gen)


@pytest.mark.asyncio
async def test_init():
    mock_session_test = MagicMock()
    student_class_repo = StudentClassRepository(mock_session_test)
    assert student_class_repo.session == mock_session_test

@pytest.mark.asyncio
async def test_get_student_class__success(studentClass_repository, mock_session):
    mock_exec_result = MagicMock() 
    mock_exec_result.first.return_value = StudentClass(
        id=1,
        student_id=1,
        class_id=1,
        points=10,
    )
    mock_session.exec = AsyncMock(return_value=mock_exec_result) 

    result = await studentClass_repository.get(1)  

    assert result.id == 1
    assert result.student_id == 1
    assert result.class_id == 1
    assert result.points == 10
    mock_session.exec.assert_awaited_once() 

@pytest.mark.asyncio
async def test_create_student_class_success(studentClass_repository, mock_session):
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    new_student_class_ = StudentClass(
        id=1,
        student_id=1,
        class_id=1,
        points=10,
    )

    result = await studentClass_repository.create(new_student_class_)

    assert result.id == 1
    assert result.points == 10
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_student_class_points_success(studentClass_repository, mock_session):
    existing_student_class_ = StudentClass(
        id=1,
        student_id=1,
        class_id=1,
        points=10,
    )

    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = existing_student_class_
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    updated_student_class_ = StudentClass(
        id=1,
        student_id=1,
        class_id=1,
        points=20,
    )

    result = await studentClass_repository.update_points(updated_student_class_)

    assert result.points == 30
    mock_session.exec.assert_awaited_once()
    mock_session.commit.assert_awaited_once() 
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_student_class_success(studentClass_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    await studentClass_repository.delete(1)

    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_awaited_once()
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_student_class_not_found(studentClass_repository, mock_session):
    mock_result_select = MagicMock()
    mock_result_select.first = MagicMock(return_value=None)
    
    mock_session.exec = AsyncMock(return_value=mock_result_select)
    mock_session.delete = AsyncMock()

    with pytest.raises(HTTPException) as exc_info:
        await studentClass_repository.delete(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Student Class not found"
    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()

@pytest.mark.asyncio
async def test_get_all_student_class__info_success(mock_session):
    fake_items = [StudentClass(id=1, class_id=2), StudentClass(id=2, class_id=2)]

    mock_exec_result = AsyncMock()
    mock_exec_result = MagicMock()
    mock_exec_result.all.return_value = fake_items
    mock_session.exec = AsyncMock(return_value=mock_exec_result)



    async def fake_session_gen():
        yield mock_session
    repo = StudentClassRepository(session=fake_session_gen)
    result = await repo.get_all(2)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2
    mock_session.exec.assert_awaited_once()
