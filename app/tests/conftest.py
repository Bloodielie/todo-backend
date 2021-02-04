from typing import AsyncGenerator, Dict

import pytest
from httpx import AsyncClient
from databases import Database
from pyject import IContainer

from app.config import DB_URL, API_PATH, first_superuser_email, first_superuser_password
from app.main import app
from app.modules.auth.dtos.token import Token


@pytest.fixture
def container() -> IContainer:
    return app.container


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    new_database = Database(DB_URL, min_size=1, max_size=1, force_rollback=True)
    app.container.override(Database, new_database)()
    await new_database.connect()
    async with AsyncClient(app=app, base_url=f"http://127.0.0.1:8000{API_PATH}") as c:
        yield c
    await new_database.disconnect()


@pytest.fixture
async def access_token(client: AsyncClient) -> Token:
    account_data = {
        "username": first_superuser_email,
        "password": first_superuser_password,
        "scope": None,
        "client_id": None,
        "client_secret": None,
    }
    r = await client.post("/auth/sign_in", data=account_data)
    return Token.parse_obj(r.json())


@pytest.fixture
async def headers(access_token: Token) -> Dict[str, str]:
    return {"Authorization": f"{access_token.token_type} {access_token.access_token}"}
