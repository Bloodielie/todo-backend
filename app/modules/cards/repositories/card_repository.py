from typing import Optional, List

from asyncpg import StringDataRightTruncationError

from app.modules.cards.dtos.card import Card, UpdateCard
from app.modules.cards.entities.card import cards
from app.modules.cards.use_cases.interfaces import ICardRepository


class CardRepository(ICardRepository):
    async def get(self, id: int) -> Optional[Card]:
        query = cards.select().where(cards.c.id == id)
        record = await self._db.fetch_one(query)
        if record is None:
            return None
        return self._mapping_record_to_model(Card, record)

    async def create(self, text: str, user_id: int) -> Optional[Card]:
        query = cards.insert().values(text=text, is_crossed_out=False, user_id=user_id).returning(*cards.columns)
        try:
            result = await self._db.fetch_one(query)
            if result is None:
                return None
            return self._mapping_record_to_model(Card, result)
        except StringDataRightTruncationError:
            return None

    async def get_by_user_id(self, user_id: int) -> Optional[List[Card]]:
        query = cards.select().where(cards.c.user_id == user_id)
        records = await self._db.fetch_all(query)
        if records is None:
            return
        return [self._mapping_record_to_model(Card, record) for record in records]

    async def delete(self, id: int) -> Optional[Card]:
        query = cards.delete().where(cards.c.id == id).returning(*cards.columns)
        result = await self._db.fetch_one(query)
        if result is not None:
            return self._mapping_record_to_model(Card, result)
        return None

    async def update(self, id: int, card: UpdateCard) -> Optional[Card]:
        query = (
            cards.update()
            .where(cards.c.id == id)
            .values(text=card.text, is_crossed_out=card.is_crossed_out)
            .returning(*cards.columns)
        )
        db_card = await self._db.fetch_one(query)
        if db_card is not None:
            return self._mapping_record_to_model(Card, db_card)
        return None

    async def search_by_text(self, text: str) -> Optional[List[Card]]:
        query = cards.select().where(cards.c.text.contains(text))
        records = await self._db.fetch_all(query)
        if not records:
            return None
        return [self._mapping_record_to_model(Card, record) for record in records]
