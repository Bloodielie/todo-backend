import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    password: str
    user_name: Optional[str]
    create_date: datetime.datetime
