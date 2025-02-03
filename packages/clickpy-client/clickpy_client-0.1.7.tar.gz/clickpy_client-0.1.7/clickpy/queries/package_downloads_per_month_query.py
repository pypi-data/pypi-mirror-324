from typing import ClassVar

from pydantic import BaseModel

from clickpy.queries.base import BaseClickPyQuery


class PackageDownloadsPerMonthModel(BaseModel):
    month: str
    count: int


class PackageDownloadsPerMonthQuery(BaseClickPyQuery[list[PackageDownloadsPerMonthModel]]):
    QUERY: ClassVar = """
SELECT
    month,
    count
FROM
    pypi.pypi_downloads_per_month
WHERE
    project = '{package}'
"""

    # Request params
    package: str
