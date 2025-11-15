from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
import pytest

from src.infrastructure.entities.users.parents import Parent
from src.infrastructure.entities.users.user import User
from src.infrastructure.repositories.parent import ParentRepository


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    session.delete = AsyncMock()
    session.exec = AsyncMock()
    return session

@pytest.fixture
def parent_repository(mock_session):
    async def session_gen():
        yield mock_session

    return ParentRepository(session=session_gen)

@pytest.fixture
def fake_parent():
    return Parent(id=1, user_id=1, student_id=1)    

@pytest.mark.asyncio
async def test_init():
    mock_session_test = MagicMock()
    parent_repository = ParentRepository(mock_session_test)
    assert parent_repository.session == mock_session_test

@pytest.mark.asyncio
async def test_get_parent_success(parent_repository, mock_session, fake_parent):
    mock_result = MagicMock()
    mock_result.all = MagicMock(return_value=[fake_parent])
    mock_session.exec = AsyncMock(return_value=mock_result)

    result = await parent_repository.get(user_id=1)

    assert isinstance(result, list)
    assert result[0].user_id == 1
    assert result[0].student_id == 1
    assert result[0].id == 1
    mock_session.exec.assert_awaited_once()

@pytest.mark.asyncio
async def test_create_parent_success(parent_repository, mock_session, fake_parent):
    
    async def mock_refresh_parent(parent):
        parent.id = 1
    mock_session.refresh = AsyncMock(side_effect=mock_refresh_parent)
    
    result = await parent_repository.create(fake_parent)

    assert isinstance(result, Parent)
    assert result.user_id == 1
    assert result.student_id == 1
    assert result.id == 1
    mock_session.add.assert_called_once_with(fake_parent)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(fake_parent)

@pytest.mark.asyncio
async def test_delete_parent_success(parent_repository, mock_session, fake_parent):
    mock_result_select = MagicMock()
    mock_result_select.first = MagicMock(return_value=fake_parent)
    
    mock_result_delete = MagicMock()
    mock_session.exec = AsyncMock(side_effect=[mock_result_select, mock_result_delete])

    result = await parent_repository.delete(user_id=1, student_id=1)

    assert result is True
    assert mock_session.exec.await_count == 2 
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_parent_not_found(parent_repository, mock_session):
    mock_result_select = MagicMock()
    mock_result_select.first = MagicMock(return_value=None)
    
    mock_session.exec = AsyncMock(return_value=mock_result_select)

    with pytest.raises(HTTPException) as exc_info:
         await parent_repository.delete(user_id=999, student_id=999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Parent not found" 
    mock_session.exec.assert_awaited_once()
    mock_session.commit.assert_not_awaited()

@pytest.mark.asyncio
async def test_get_parent_not_found(parent_repository, mock_session):
    mock_result = MagicMock()
    mock_result.all = MagicMock(return_value=[])
    mock_session.exec = AsyncMock(return_value=mock_result)

    with pytest.raises(HTTPException) as exc_info:
        await parent_repository.get(user_id=999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Parent not found"
    mock_session.exec.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_all_parents_success():
    fake_users = [
        User(id=1, name="John", last_name="Doe", dni="123", phone="111", email="a@test.com", username="john", role_id=4),
        User(id=2, name="Jane", last_name="Doe", dni="456", phone="222", email="b@test.com", username="jane", role_id=4),
    ]
    fake_parents = [
        Parent(id=1, user_id=1, student_id=101),
        Parent(id=2, user_id=1, student_id=102),
        Parent(id=3, user_id=2, student_id=103),
    ]

    mock_session = AsyncMock()

    async def exec_coroutine(statement, *args, **kwargs):
        stmt_str = str(statement)
        if "WHERE" in stmt_str and "role_id" in stmt_str:
            mock_exec_users = MagicMock()
            mock_exec_users.all.return_value = fake_users
            return mock_exec_users
        elif "FROM parents" in stmt_str:
            mock_exec_parents = MagicMock()
            mock_exec_parents.all.return_value = fake_parents
            return mock_exec_parents
        else:
            raise ValueError("Unexpected statement")

    mock_session.exec.side_effect = exec_coroutine

    async def fake_session_gen():
        yield mock_session

    repo = ParentRepository(session=fake_session_gen)
    result = await repo.get_all()

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0].user_id == 1
    assert result[0].students == [101, 102]

    assert result[1].user_id == 2
    assert result[1].students == [103]

    assert mock_session.exec.await_count == 2