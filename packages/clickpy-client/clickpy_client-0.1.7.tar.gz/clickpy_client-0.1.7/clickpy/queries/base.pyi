from _typeshed import Incomplete
from pydantic import BaseModel
from typing import Any, ClassVar, Generic, TypeVar

TModel = TypeVar('TModel')

class BaseClickPyQuery(BaseModel, Generic[TModel]):
    Model = TModel
    QUERY: ClassVar[str]
    class Config:
        ignored_types: Incomplete
    def __init_subclass__(cls, **kwargs: Any): ...
    def query(self) -> str: ...
