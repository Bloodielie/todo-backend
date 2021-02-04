import pytest
from httpx import AsyncClient

from app.modules.cards.dtos.card import Card


async def create_task(client: AsyncClient, headers) -> Card:
    task_data = {"text": "test"}
    r = await client.post("/task/", headers=headers, json=task_data)
    assert r.status_code == 201
    return Card.parse_obj(r.json())


@pytest.mark.asyncio
async def test_get_tasks(client: AsyncClient, headers) -> None:
    r = await client.get("/task/")
    assert r.status_code == 401

    r = await client.get("/task/", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        assert isinstance(data[0], dict)
        task = Card.parse_obj(data[0])
        assert isinstance(task, Card)


@pytest.mark.asyncio
async def test_get_task(client: AsyncClient, headers) -> None:
    r = await client.get("/task/1")
    assert r.status_code == 401

    task = await create_task(client, headers)
    r = await client.get(f"/task/{task.id}", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    task = Card.parse_obj(data)
    assert isinstance(task, Card)


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, headers) -> None:
    task_data = {"text": "test"}

    r = await client.post("/task/", json=task_data)
    assert r.status_code == 401

    r = await client.post("/task/", headers=headers, json=task_data)
    assert r.status_code == 201
    data = r.json()
    assert isinstance(data, dict)
    task = Card.parse_obj(data)
    assert isinstance(task, Card)


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, headers) -> None:
    task = await create_task(client, headers)

    r = await client.delete(f"/task/{task.id}", headers=headers)
    assert r.status_code == 200

    r = await client.delete(f"/task/{task.id}", headers=headers)
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient, headers) -> None:
    task = await create_task(client, headers)

    update_task_data = {"text": "12333", "is_crossed_out": False}

    r = await client.patch(f"/task/{task.id}", headers=headers, json=update_task_data)
    assert r.status_code == 200

    r = await client.patch(f"/task/{task.id+1}", headers=headers, json=update_task_data)
    assert r.status_code == 404
