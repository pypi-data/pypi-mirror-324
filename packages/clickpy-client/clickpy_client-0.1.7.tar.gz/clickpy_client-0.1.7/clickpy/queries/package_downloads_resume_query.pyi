from clickpy.queries.base import BaseClickPyQuery as BaseClickPyQuery
from pydantic import BaseModel
from typing import ClassVar

class PackageDownloadsResumeModel(BaseModel):
    week: int
    month: int
    year: int
    total: int

class PackageDownloadsResumeQuery(BaseClickPyQuery[PackageDownloadsResumeModel]):
    QUERY: ClassVar
    package: str
