from typing import Optional

from pydantic import BaseModel


class UserData(BaseModel):
    email: str
    password: str
    user_name: Optional[str]


class UserToken(BaseModel):
    sub: str
    id: int
    exp: int
