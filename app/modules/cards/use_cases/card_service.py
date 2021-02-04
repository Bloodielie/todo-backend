from typing import Optional, List

from app.modules.cards.dtos.card import UpdateCard, Card
from app.modules.cards.use_cases.interfaces import ICardService, ICardRepository


class CardService(ICardService):
    def __init__(self, repository: ICardRepository):
        self._repository = repository

    async def get(self, id: int) -> Optional[Card]:
        return await self._repository.get(id)

    async def get_by_user_id(self, user_id: int) -> Optional[List[Card]]:
        return await self._repository.get_by_user_id(user_id)

    async def create(self, text: str, user_id: int) -> Optional[Card]:
        return await self._repository.create(text, user_id)

    async def delete(self, id: int) -> Optional[Card]:
        return await self._repository.delete(id)

    async def update(self, id: int, card: UpdateCard) -> Optional[Card]:
        return await self._repository.update(id, card)

    async def search_by_text(self, text: str) -> Optional[List[Card]]:
        return await self._repository.search_by_text(text)
