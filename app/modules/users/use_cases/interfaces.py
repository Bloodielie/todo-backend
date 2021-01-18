from typing import Optional

from app.infrastructure.database import BaseRepository
from abc import abstractmethod, ABC

from app.modules.users.dtos.user import User


class IUserRepository(BaseRepository):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create(self, email: str, password: str, user_name: Optional[str]) -> Optional[User]:
        pass


class IUserService(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create(self, email: str, password: str, user_name: Optional[str]) -> Optional[User]:
        pass
