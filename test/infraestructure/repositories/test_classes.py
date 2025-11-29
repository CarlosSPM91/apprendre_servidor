from sqlite3 import IntegrityError
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException
import pytest

from src.domain.objects.classes.subject_assignment_dto import SubjectAssignmentDTO
from src.domain.objects.classes.update_class_subjects_dto import UpdateClassSubjectsDTO
from src.infrastructure.entities.course.classes import Classes
from src.infrastructure.entities.course.subject_class import SubjectClass
from src.infrastructure.repositories.classes import ClassesRepository




@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def classes_repository(mock_session):
    async def session_gen():
        yield mock_session
    return ClassesRepository(session=session_gen)


@pytest.mark.asyncio
async def test_init():
    mock_session_test = MagicMock()
    Classes_repo = ClassesRepository(mock_session_test)
    assert Classes_repo.session == mock_session_test

@pytest.mark.asyncio
async def test_get_Classes_success(classes_repository, mock_session):
    mock_exec_result = MagicMock() 
    mock_exec_result.first.return_value = Classes(
        id=1,
        course_id=1,
        name='1erB',
    )
    mock_session.exec = AsyncMock(return_value=mock_exec_result) 

    result = await classes_repository.get_by_id(1)  

    assert result.id == 1
    assert result.course_id == 1
    assert result.name == '1erB'
    mock_session.exec.await_count == 2

@pytest.mark.asyncio
async def test_create_Classes_success(classes_repository, mock_session):
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    new_Classes = Classes(
        course_id=1,
        name='1erB',
    )

    result = await classes_repository.create(new_Classes)

    assert result.course_id == 1
    assert result.name == '1erB'
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_classes_success(classes_repository, mock_session):
    existing_Classes = Classes(
        id=1,
        course_id=1,
        name='1erB',
    )

    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = existing_Classes
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    updated_Classes = Classes(
        id=1,
        course_id=2,
        name='1erA',
    )

    result = await classes_repository.update(updated_Classes)

    assert result.id == 1
    assert result.course_id == 2
    assert result.name == '1erA'
    mock_session.exec.assert_awaited_once()
    mock_session.commit.assert_awaited_once() 
    mock_session.refresh.assert_awaited_once() 

@pytest.mark.asyncio
async def test_update_classes_not_found(classes_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = None
    mock_session.exec = AsyncMock(return_value=mock_exec_result)

    non_existent_Classes = Classes(
        id=999,
        course_id=2,
        name='1erA',
    )

    with pytest.raises(Exception) as exc_info:
        await classes_repository.update(non_existent_Classes)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Classes not found"
    mock_session.exec.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_classes_success(classes_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    await classes_repository.delete(1)

    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_awaited_once()
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_classes_not_found(classes_repository, mock_session):
    mock_result_select = MagicMock()
    mock_result_select.first = MagicMock(return_value=None)
    
    mock_session.exec = AsyncMock(return_value=mock_result_select)
    mock_session.delete = AsyncMock()

    with pytest.raises(HTTPException) as exc_info:
        await classes_repository.delete(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Classes not found"
    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()

@pytest.mark.asyncio
async def test_get_all_classes_info_success(mock_session):
    fake_items = [Classes(id=1), Classes(id=2)]

    mock_exec_result = AsyncMock()
    mock_exec_result = MagicMock()
    mock_exec_result.all.return_value = fake_items
    mock_session.exec = AsyncMock(return_value=mock_exec_result)



    async def fake_session_gen():
        yield mock_session
    repo = ClassesRepository(session=fake_session_gen)
    result = await repo.get_all()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2
    mock_session.exec.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_subjects_success(classes_repository, mock_session):

    existing_class = Classes(
        id=1,
        course_id=1,
        name="1erB",
        tutor_id=5,
    )

    mock_exec_select_class = MagicMock()
    mock_exec_select_class.first.return_value = existing_class


    mock_exec_delete = AsyncMock()

    mock_exec_select_subjects = MagicMock()
    mock_exec_select_subjects.all.return_value = [
        SubjectAssignmentDTO(subject_id=10, class_id=1, teacher_id=100),
        SubjectAssignmentDTO(subject_id=20, class_id=1, teacher_id=200),
    ]

    mock_session.exec = AsyncMock(side_effect=[
        mock_exec_select_class,
        mock_exec_delete,
        mock_exec_select_subjects,
    ])

    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    mock_session.add = MagicMock()

    update_dto = UpdateClassSubjectsDTO(
        class_id=1,
        subjects=[
            SubjectAssignmentDTO(subject_id=10, teacher_id=100),
            SubjectAssignmentDTO(subject_id=20, teacher_id=200),
        ],
    )

    result = await classes_repository.update_subjects(update_dto)

    assert result.id == 1
    assert result.name == "1erB"
    assert result.subjects == [10, 20]

    assert mock_session.exec.await_count == 3
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_subjects_class_not_found(classes_repository, mock_session):

    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = None
    mock_session.exec = AsyncMock(return_value=mock_exec_result)

    update_dto = UpdateClassSubjectsDTO(
        class_id=999,
        subjects=[]
    )

    with pytest.raises(HTTPException) as exc:
        await classes_repository.update_subjects(update_dto)

    assert exc.value.status_code == 404

