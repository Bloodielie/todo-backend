import pytest
from httpx import AsyncClient
from pyject import IContainer

from app.config import first_superuser_email, first_superuser_password
from app.modules.auth.dtos.token import Token
from app.modules.auth.use_cases.interfaces import IJwtService


def validate_token(data: dict, container: IContainer) -> None:
    assert isinstance(data, dict)
    token_model = Token.parse_obj(data)
    assert isinstance(token_model, Token)
    assert isinstance(token_model.access_token, str)
    assert isinstance(token_model.token_type, str)
    jwt_service = container.get(IJwtService)
    access_token_data = jwt_service.decode_access_token(token_model.access_token)
    assert isinstance(access_token_data["sub"], str)


@pytest.mark.asyncio
async def test_register(client: AsyncClient, container: IContainer) -> None:
    account_data = {"email": "roma@gmail2.com", "password": "1234", "user_name": "1234"}
    r = await client.post("/auth/register", json=account_data)
    assert r.status_code == 201
    validate_token(r.json(), container)

    r = await client.post(f"/auth/register", json=account_data)
    assert r.status_code == 400
    response = r.json()
    assert isinstance(response, dict)
    assert isinstance(response["detail"], str)


@pytest.mark.asyncio
async def test_sign_in(client: AsyncClient, container: IContainer) -> None:
    base_account_data = {"scope": None, "client_id": None, "client_secret": None}

    valid_account_data = {
        "username": first_superuser_email,
        "password": first_superuser_password,
    }
    valid_account_data.update(base_account_data)
    r = await client.post("/auth/sign_in", data=valid_account_data)
    assert r.status_code == 200
    validate_token(r.json(), container)

    invalid_account_data = {
        "username": first_superuser_email + "1",
        "password": first_superuser_password,
    }
    invalid_account_data.update(base_account_data)
    r = await client.post("/auth/sign_in", data=invalid_account_data)
    assert r.status_code == 401
    assert r.json()["detail"] == "Incorrect username"

    invalid_account_data2 = {
        "username": first_superuser_email,
        "password": first_superuser_password + "1",
    }
    invalid_account_data2.update(base_account_data)
    r = await client.post("/auth/sign_in", data=invalid_account_data2)
    assert r.status_code == 401
    assert r.json()["detail"] == "Incorrect password"
