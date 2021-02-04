from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from app.infrastructure.database import BaseRepository
from app.modules.auth.dtos.token import RefreshTokenInDb


class IRefreshTokenRepository(BaseRepository):
    @abstractmethod
    async def create(self, token: str, user_id: int) -> Optional[RefreshTokenInDb]:
        pass

    @abstractmethod
    async def get_by_token(self, token: str) -> Optional[RefreshTokenInDb]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[RefreshTokenInDb]:
        pass

    @abstractmethod
    async def delete_by_user_id(self, user_id: int) -> Optional[RefreshTokenInDb]:
        pass

    @abstractmethod
    async def delete_by_token(self, token: str) -> Optional[RefreshTokenInDb]:
        pass


class IRefreshTokenService(ABC):
    @abstractmethod
    async def get_by_token(self, token: str) -> Optional[RefreshTokenInDb]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[RefreshTokenInDb]:
        pass

    @abstractmethod
    async def delete_by_user_id(self, user_id: int) -> Optional[RefreshTokenInDb]:
        pass

    @abstractmethod
    async def delete_by_token(self, token: str) -> Optional[RefreshTokenInDb]:
        pass

    @abstractmethod
    async def create(self, token: str, user_id: int) -> Optional[RefreshTokenInDb]:
        pass


class IJwtService(ABC):
    @abstractmethod
    def create_access_token(self, data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        pass


class IPasswordHashService(ABC):
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        pass
