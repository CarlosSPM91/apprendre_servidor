from sqlite3 import IntegrityError
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException
import pytest

from src.infrastructure.entities.course.student_class import StudentClass
from src.infrastructure.entities.course.subject_class import SubjectClass
from src.infrastructure.repositories.subject_class import SubjectClassRepository



@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def subject_class_repo(mock_session):
    async def session_gen():
        yield mock_session
    return SubjectClassRepository(session=session_gen)


@pytest.mark.asyncio
async def test_init():
    mock_session_test = MagicMock()
    student_class_repo = SubjectClassRepository(mock_session_test)
    assert student_class_repo.session == mock_session_test

@pytest.mark.asyncio
async def test_get_subject_class__success(subject_class_repo, mock_session):
    mock_exec_result = MagicMock() 
    mock_exec_result.first.return_value = SubjectClass(
        id=1,
        class_id=1,
        professor_id=1,
        subject_id=1,
    )
    mock_session.exec = AsyncMock(return_value=mock_exec_result) 

    result = await subject_class_repo.get(1)  

    assert result.id == 1
    assert result.class_id == 1
    assert result.professor_id == 1
    mock_session.exec.assert_awaited_once() 

@pytest.mark.asyncio
async def test_create_subject_class_success(subject_class_repo, mock_session):
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    new_subject_class_ = SubjectClass(
        id=1,
        class_id=1,
        professor_id=1,
        subject_id=1,
    )

    result = await subject_class_repo.create(new_subject_class_)

    assert result.id == 1
    assert result.class_id == 1
    assert result.professor_id == 1
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_subject_class_success(subject_class_repo, mock_session):
    existing_subject_class_ = SubjectClass(
        id=1,
        class_id=1,
        professor_id=1,
        subject_id=1,
    )

    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = existing_subject_class_
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    updated_subject_class_ = SubjectClass(
        id=1,
        class_id=1,
        professor_id=1,
        subject_id=2,
    )

    result = await subject_class_repo.update(updated_subject_class_)

    assert result.subject_id == 2
    mock_session.exec.assert_awaited_once()
    mock_session.commit.assert_awaited_once() 
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_subject_class_success(subject_class_repo, mock_session):
    mock_exec_result = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    await subject_class_repo.delete(1)

    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_awaited_once()
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_subject_class_not_found(subject_class_repo, mock_session):
    mock_result_select = MagicMock()
    mock_result_select.first = MagicMock(return_value=None)
    
    mock_session.exec = AsyncMock(return_value=mock_result_select)
    mock_session.delete = AsyncMock()

    with pytest.raises(HTTPException) as exc_info:
        await subject_class_repo.delete(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Subject Class not found"
    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()

@pytest.mark.asyncio
async def test_get_all_subject_class__info_success(mock_session):
    fake_items = [SubjectClass(id=1), StudentClass(id=2)]

    mock_exec_result = AsyncMock()
    mock_exec_result = MagicMock()
    mock_exec_result.all.return_value = fake_items
    mock_session.exec = AsyncMock(return_value=mock_exec_result)



    async def fake_session_gen():
        yield mock_session
    repo = SubjectClassRepository(session=fake_session_gen)
    result = await repo.get_all()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2
    mock_session.exec.assert_awaited_once()
