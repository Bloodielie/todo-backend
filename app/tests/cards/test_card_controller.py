from typing import Dict

import pytest
from httpx import AsyncClient

from app.config import first_superuser_email, first_superuser_password
from app.modules.auth.dtos.token import Token
from app.modules.cards.dtos.card import Card


async def get_access_token(client: AsyncClient) -> Token:
    account_data = {
        "username": first_superuser_email,
        "password": first_superuser_password,
        "scope": None,
        "client_id": None,
        "client_secret": None,
    }
    r = await client.post("/auth/sign_in", data=account_data)
    return Token.parse_obj(r.json())


async def get_token_header(client: AsyncClient) -> Dict[str, str]:
    token = await get_access_token(client)
    return {"Authorization": f"{token.token_type} {token.access_token}"}


async def create_card(client: AsyncClient) -> Card:
    access_token_header = await get_token_header(client)
    card_data = {"text": "test"}
    r = await client.post("/card/", headers=access_token_header, json=card_data)
    assert r.status_code == 201
    return Card.parse_obj(r.json())


@pytest.mark.asyncio
async def test_get_cards(client: AsyncClient) -> None:
    r = await client.get("/card/")
    assert r.status_code == 401

    access_token_header = await get_token_header(client)

    r = await client.get("/card/", headers=access_token_header)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        assert isinstance(data[0], dict)
        card = Card.parse_obj(data[0])
        assert isinstance(card, Card)


@pytest.mark.asyncio
async def test_get_card(client: AsyncClient) -> None:
    r = await client.get("/card/1")
    assert r.status_code == 401

    access_token_header = await get_token_header(client)
    card = await create_card(client)
    r = await client.get(f"/card/{card.id}", headers=access_token_header)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    card = Card.parse_obj(data)
    assert isinstance(card, Card)


@pytest.mark.asyncio
async def test_create_card(client: AsyncClient) -> None:
    card_data = {"text": "test"}

    r = await client.post("/card/", json=card_data)
    assert r.status_code == 401

    access_token_header = await get_token_header(client)

    r = await client.post("/card/", headers=access_token_header, json=card_data)
    assert r.status_code == 201
    data = r.json()
    assert isinstance(data, dict)
    card = Card.parse_obj(data)
    assert isinstance(card, Card)


@pytest.mark.asyncio
async def test_delete_card(client: AsyncClient) -> None:
    access_token_header = await get_token_header(client)
    card = await create_card(client)

    r = await client.delete(f"/card/{card.id}", headers=access_token_header)
    assert r.status_code == 200

    r = await client.delete(f"/card/{card.id}", headers=access_token_header)
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_update_card(client: AsyncClient) -> None:
    access_token_header = await get_token_header(client)
    card = await create_card(client)

    update_card_data = {"text": "12333", "is_crossed_out": False}

    r = await client.patch(f"/card/{card.id}", headers=access_token_header, json=update_card_data)
    assert r.status_code == 200

    r = await client.patch(f"/card/{card.id+1}", headers=access_token_header, json=update_card_data)
    assert r.status_code == 404
