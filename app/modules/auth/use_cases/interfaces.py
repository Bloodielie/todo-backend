from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class IJwtService(ABC):
    @abstractmethod
    def create_access_token(self, data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def decode_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        pass


class IPasswordHashService(ABC):
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        pass
