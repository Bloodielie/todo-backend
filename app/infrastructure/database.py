from abc import ABC
from typing import Any, TypeVar, Type

from databases import Database
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(ABC):
    def __init__(self, db: Database):
        self._db = db

    def _mapping_record_to_model(self, model: Type[T], data: Any) -> T:
        return model.parse_obj(dict(data))
