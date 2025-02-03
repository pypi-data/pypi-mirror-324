from clickpy.queries.base import BaseClickPyQuery as BaseClickPyQuery
from pydantic import BaseModel
from typing import ClassVar

class KeywordsByReleasesModel(BaseModel):
    name: str
    releases: int

class KeywordsByReleasesQuery(BaseClickPyQuery[list[KeywordsByReleasesModel]]):
    QUERY: ClassVar
    limit: int
    offset: int
    def query(self) -> str: ...
