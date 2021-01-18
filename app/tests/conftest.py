from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from databases import Database
from pyject import IContainer

from app.config import DB_URL, API_PATH
from app.main import app


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
