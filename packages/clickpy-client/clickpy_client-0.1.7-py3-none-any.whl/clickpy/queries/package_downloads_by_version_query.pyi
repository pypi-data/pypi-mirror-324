from clickpy.queries.base import BaseClickPyQuery as BaseClickPyQuery
from pydantic import BaseModel
from typing import ClassVar

class PackageDownloadsByVersionModel(BaseModel):
    version: str
    count: int

class PackageDownloadsByVersionQuery(BaseClickPyQuery[PackageDownloadsByVersionModel]):
    QUERY: ClassVar
    package: str
