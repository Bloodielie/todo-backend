from typing import Optional

from asyncpg import UniqueViolationError

from app.modules.users.dtos.user import User
from app.modules.users.entities.user import users
from app.modules.users.use_cases.interfaces import IUserRepository


class UserRepository(IUserRepository):
    async def get_by_email(self, email: str) -> Optional[User]:
        query = users.select().where(users.c.email == email)
        record = await self._db.fetch_one(query)
        if record is None:
            return None
        return self._mapping_record_to_model(User, record)

    async def create(self, email: str, password: str, user_name: Optional[str]) -> Optional[User]:
        query = users.insert().values(email=email, password=password, user_name=user_name).returning(*users.columns)
        try:
            result = await self._db.fetch_one(query)
            if result is None:
                return None
            return self._mapping_record_to_model(User, result)
        except UniqueViolationError:
            return None
