import datetime
from typing import Optional

from pydantic import BaseModel


class Check(BaseModel):
    status: bool


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    username: Optional[str] = None


class CreateRefreshToken(BaseModel):
    token: str
    user_id: int


class RefreshTokenInDb(BaseModel):
    id: int
    token: str
    user_id: int
    create_date: datetime.datetime
