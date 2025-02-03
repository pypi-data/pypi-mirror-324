from clickpy.queries.base import BaseClickPyQuery as BaseClickPyQuery
from pydantic import BaseModel
from typing import ClassVar

class PackageDownloadsPerMonthModel(BaseModel):
    month: str
    count: int

class PackageDownloadsPerMonthQuery(BaseClickPyQuery[list[PackageDownloadsPerMonthModel]]):
    QUERY: ClassVar
    package: str
