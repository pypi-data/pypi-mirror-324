from clickpy.queries.base import BaseClickPyQuery as BaseClickPyQuery
from pydantic import BaseModel
from typing import ClassVar

class PackageReleasesResumeModel(BaseModel):
    week: int
    month: int
    year: int
    total: int

class PackageReleasesResumeQuery(BaseClickPyQuery[PackageReleasesResumeModel]):
    QUERY: ClassVar
    package: str
