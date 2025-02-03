from clickpy.queries.base import BaseClickPyQuery as BaseClickPyQuery
from pydantic import BaseModel
from typing import ClassVar

class KeywordReleasesResumeModel(BaseModel):
    week: int
    month: int
    year: int
    total: int

class KeywordReleasesResumeQuery(BaseClickPyQuery[KeywordReleasesResumeModel]):
    QUERY: ClassVar
    keyword: str
