from databases import Database
from typing import Callable, Awaitable

from app.config import first_superuser_email, first_superuser_password
from app.modules.auth.use_cases.passwordhash_service import PasswordHashService
from app.modules.users.repositories.user_repository import UserRepository
from app.modules.auth.repositories.refresh_token_repository import RefreshTokenRepository
from app.modules.auth.use_cases.jwt_service import JwtService


async def init_db(database: Database):
    user_repository = UserRepository(database)
    refresh_token_repository = RefreshTokenRepository(database)
    jwt_service = JwtService()
    user = await user_repository.get_by_email(first_superuser_email)
    if user is None:
        password_hash = PasswordHashService()
        user = await user_repository.create(
            first_superuser_email, password_hash.get_password_hash(first_superuser_password), "admin"
        )
        data = {"sub": user.email, "id": user.id}
        refresh_token = jwt_service.create_refresh_token(data)
        await refresh_token_repository.create(user_id=user.id, token=refresh_token)


def on_startup(database: Database) -> Callable[[], Awaitable[None]]:
    async def on_startup_handler() -> None:
        await database.connect()
        await init_db(database)

    return on_startup_handler


def on_shutdown(database: Database) -> Callable[[], Awaitable[None]]:
    async def on_shutdown_handler() -> None:
        await database.disconnect()

    return on_shutdown_handler
