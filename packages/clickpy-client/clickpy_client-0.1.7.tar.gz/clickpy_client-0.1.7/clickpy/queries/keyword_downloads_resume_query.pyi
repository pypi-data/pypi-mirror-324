from clickpy.queries.base import BaseClickPyQuery as BaseClickPyQuery
from pydantic import BaseModel
from typing import ClassVar

class KeywordDownloadsResumeModel(BaseModel):
    week: int
    month: int
    year: int
    total: int

class KeywordDownloadsResumeQuery(BaseClickPyQuery[KeywordDownloadsResumeModel]):
    QUERY: ClassVar
    keyword: str
