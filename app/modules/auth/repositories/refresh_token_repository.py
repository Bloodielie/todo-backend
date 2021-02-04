from typing import Optional

from app.modules.auth.dtos.token import RefreshTokenInDb
from app.modules.auth.entities.refresh_token import refresh_token
from app.modules.auth.use_cases.interfaces import IRefreshTokenRepository


class RefreshTokenRepository(IRefreshTokenRepository):
    async def get_by_token(self, token: str) -> Optional[RefreshTokenInDb]:
        query = refresh_token.select().where(refresh_token.c.token == token)
        record = await self._db.fetch_one(query)
        if record is None:
            return None
        return self._mapping_record_to_model(RefreshTokenInDb, record)

    async def get_by_user_id(self, user_id: int) -> Optional[RefreshTokenInDb]:
        query = refresh_token.select().where(refresh_token.c.user_id == user_id)
        record = await self._db.fetch_one(query)
        if record is None:
            return None
        return self._mapping_record_to_model(RefreshTokenInDb, record)

    async def delete_by_user_id(self, user_id: int) -> Optional[RefreshTokenInDb]:
        query = refresh_token.delete().where(refresh_token.c.user_id == user_id).returning(*refresh_token.columns)
        result = await self._db.fetch_one(query)
        if result is None:
            return None
        return self._mapping_record_to_model(RefreshTokenInDb, result)

    async def delete_by_token(self, token: str) -> Optional[RefreshTokenInDb]:
        query = refresh_token.delete().where(refresh_token.c.token == token).returning(*refresh_token.columns)
        result = await self._db.fetch_one(query)
        if result is None:
            return None
        return self._mapping_record_to_model(RefreshTokenInDb, result)

    async def create(self, token: str, user_id: int) -> Optional[RefreshTokenInDb]:
        query = refresh_token.insert().values(token=token, user_id=user_id).returning(*refresh_token.columns)
        result = await self._db.fetch_one(query)
        if result is None:
            return None
        return self._mapping_record_to_model(RefreshTokenInDb, result)
