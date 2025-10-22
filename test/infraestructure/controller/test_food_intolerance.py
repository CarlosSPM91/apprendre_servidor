from unittest.mock import AsyncMock
from fastapi import HTTPException
import pytest

from src.infrastructure.controllers.food_intolrance import FoodIntoleranceController
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance


@pytest.fixture
def create_case():
    mock = AsyncMock()
    return mock


@pytest.fixture
def update_case():
    mock = AsyncMock()
    return mock


@pytest.fixture
def delete_case():
    mock = AsyncMock()
    return mock


@pytest.fixture
def find_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def fake_intolerance():
    return FoodIntolerance(
        id=1,
        user_id=1,
        observations="Test observations",
    )

@pytest.fixture
def food_controller(find_case, create_case, update_case, delete_case):
    return FoodIntoleranceController(
        find_case=find_case,
        create_case=create_case,
        update_case=update_case,
        delete_case=delete_case,
    )

@pytest.mark.asyncio
async def test_init_food_controller(
    food_controller,
    find_case,
    create_case,
    update_case,
    delete_case,
):
    assert food_controller.find_intolerance_case == find_case
    assert food_controller.create_intolerance_case == create_case
    assert food_controller.update_intolerance_case == update_case
    assert food_controller.delete_intolerance_case == delete_case

@pytest.mark.asyncio
async def test_create_food_intolerance(
    food_controller,
    create_case,
    fake_intolerance,
):
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2024-01-01T00:00:00Z"
    create_case.create.return_value = mock_resp

    response = await food_controller.create(fake_intolerance)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_resp.item_id)

@pytest.mark.asyncio
async def test_update_food_intolerance(
    food_controller,
    find_case,
    update_case,
    fake_intolerance,
):
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2024-02-01T00:00:00Z"
    find_case.get_intolerance.return_value = fake_intolerance
    update_case.update.return_value = mock_resp

    response = await food_controller.update(fake_intolerance)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_resp.item_id)

@pytest.mark.asyncio
async def test_delete_food_intolerance(
    food_controller,
    find_case,
    delete_case,
):
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2024-03-01T00:00:00Z"
    find_case.get_intolerance.return_value = AsyncMock()
    delete_case.delete.return_value = mock_resp

    response = await food_controller.delete(intolerance_id=1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_resp.item_id)

@pytest.mark.asyncio
async def test_get_food_intolerance(
    food_controller,
    find_case,
    fake_intolerance,
):
    find_case.get_intolerance.return_value = fake_intolerance

    response = await food_controller.get_intolerance(intolernce_id=1)

    assert response == fake_intolerance
    find_case.get_intolerance.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_get_food_intolerance_not_found(
    food_controller,
    find_case,
): 
    find_case.get_intolerance.side_effect = HTTPException(status_code=404, detail="Not Found")

    with pytest.raises(HTTPException):
        await food_controller.get_intolerance(intolernce_id=999)

    find_case.get_intolerance.assert_awaited_once_with(999)


