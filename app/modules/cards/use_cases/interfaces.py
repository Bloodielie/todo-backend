from abc import abstractmethod, ABC
from typing import Optional, List

from app.modules.cards.dtos.card import Card, UpdateCard
from app.infrastructure.database import BaseRepository


class ICardRepository(BaseRepository):
    @abstractmethod
    async def get(self, id: int) -> Optional[Card]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[List[Card]]:
        pass

    @abstractmethod
    async def create(self, text: str, user_id: int) -> Optional[Card]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> Optional[Card]:
        pass

    @abstractmethod
    async def update(self, id: int, card: UpdateCard) -> Optional[Card]:
        pass

    @abstractmethod
    async def search_by_text(self, text: str) -> Optional[List[Card]]:
        pass


class ICardService(ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[Card]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[List[Card]]:
        pass

    @abstractmethod
    async def create(self, text: str, user_id: int) -> Optional[Card]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> Optional[Card]:
        pass

    @abstractmethod
    async def update(self, id: int, card: UpdateCard) -> Optional[Card]:
        pass

    @abstractmethod
    async def search_by_text(self, text: str) -> Optional[List[Card]]:
        pass
