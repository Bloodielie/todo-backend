from typing import Optional

from app.modules.auth.dtos.token import RefreshTokenInDb
from app.modules.auth.use_cases.interfaces import IRefreshTokenService, IRefreshTokenRepository


class RefreshTokenService(IRefreshTokenService):
    def __init__(self, refresh_token_repository: IRefreshTokenRepository):
        self._refresh_token_repository = refresh_token_repository

    async def get_by_token(self, token: str) -> Optional[RefreshTokenInDb]:
        return await self._refresh_token_repository.get_by_token(token)

    async def get_by_user_id(self, user_id: int) -> Optional[RefreshTokenInDb]:
        return await self._refresh_token_repository.get_by_user_id(user_id)

    async def delete_by_user_id(self, user_id: int) -> Optional[RefreshTokenInDb]:
        return await self._refresh_token_repository.delete_by_user_id(user_id)

    async def create(self, token: str, user_id: int) -> Optional[RefreshTokenInDb]:
        return await self._refresh_token_repository.create(token, user_id)
    
    async def delete_by_token(self, token: str) -> Optional[RefreshTokenInDb]:
        return await self._refresh_token_repository.delete_by_token(token)
