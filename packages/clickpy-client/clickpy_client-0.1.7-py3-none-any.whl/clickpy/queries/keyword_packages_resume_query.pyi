from clickpy.queries.base import BaseClickPyQuery as BaseClickPyQuery
from pydantic import BaseModel
from typing import ClassVar

class KeywordPackagesResumeModel(BaseModel):
    week: int
    month: int
    year: int
    total: int

class KeywordPackagesResumeQuery(BaseClickPyQuery[KeywordPackagesResumeModel]):
    QUERY: ClassVar
    keyword: str
