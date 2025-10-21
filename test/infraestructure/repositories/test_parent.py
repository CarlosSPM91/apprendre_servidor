from unittest.mock import AsyncMock, MagicMock
import pytest

from src.infrastructure.entities.users.parents import Parent
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