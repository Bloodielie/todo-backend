from typing import Optional

from app.modules.auth.use_cases.interfaces import IPasswordHashService
from app.modules.users.dtos.user import User
from app.modules.users.use_cases.interfaces import IUserService, IUserRepository


class UserService(IUserService):
    def __init__(self, repository: IUserRepository, password_hash_service: IPasswordHashService) -> None:
        self._repository = repository
        self._password_hash_service = password_hash_service

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self._repository.get_by_email(email)

    async def create(self, email: str, password: str, user_name: Optional[str]) -> Optional[User]:
        hashed_password = self._password_hash_service.get_password_hash(password)
        return await self._repository.create(email, hashed_password, user_name)

    async def get_by_id(self, id: int) -> Optional[User]:
        return await self._repository.get_by_id(id)
