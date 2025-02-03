from typing import ClassVar

from pydantic import BaseModel

from clickpy.queries.base import BaseClickPyQuery


class PackageDownloadsByVersionModel(BaseModel):
    version: str
    count: int


class PackageDownloadsByVersionQuery(BaseClickPyQuery[PackageDownloadsByVersionModel]):
    QUERY: ClassVar = """
SELECT
    version,
    count
FROM
    pypi.pypi_downloads_by_version
WHERE
    project = '{package}'
"""

    # Request params
    package: str
