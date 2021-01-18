from databases import Database
from typing import Callable, Awaitable

from app.config import first_superuser_email, first_superuser_password
from app.modules.auth.use_cases.passwordhash_service import PasswordHashService
from app.modules.users.repositories.user_repository import UserRepository


async def init_db(database: Database):
    user_repository = UserRepository(database)
    user = await user_repository.get_by_email(first_superuser_email)
    password_hash = PasswordHashService()
    if user is None:
        await user_repository.create(
            first_superuser_email, password_hash.get_password_hash(first_superuser_password), "admin"
        )


def on_startup(database: Database) -> Callable[[], Awaitable[None]]:
    async def on_startup_handler() -> None:
        await database.connect()
        await init_db(database)

    return on_startup_handler


def on_shutdown(database: Database) -> Callable[[], Awaitable[None]]:
    async def on_shutdown_handler() -> None:
        await database.disconnect()

    return on_shutdown_handler
