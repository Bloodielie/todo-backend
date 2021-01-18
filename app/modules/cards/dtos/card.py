import datetime

from pydantic import BaseModel


class CreateCard(BaseModel):
    text: str


class UpdateCard(BaseModel):
    text: str
    is_crossed_out: bool


class Card(UpdateCard):
    id: int
    create_date: datetime.datetime
    user_id: int
