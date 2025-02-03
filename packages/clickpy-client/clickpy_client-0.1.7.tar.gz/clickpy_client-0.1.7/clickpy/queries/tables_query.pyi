from clickpy.queries.base import BaseClickPyQuery as BaseClickPyQuery
from datetime import datetime
from pydantic import BaseModel
from typing import ClassVar
from uuid import UUID

class TableModel(BaseModel):
    database: str
    name: str
    uuid: UUID
    engine: str
    is_temporary: int
    data_paths: list[str]
    metadata_path: str
    metadata_modification_time: datetime
    metadata_version: int
    dependencies_database: list[str]
    dependencies_table: list[str]
    create_table_query: str
    engine_full: str
    as_select: str
    partition_key: str
    sorting_key: str
    primary_key: str
    sampling_key: str
    storage_policy: str
    total_rows: int | None
    total_bytes: int | None
    total_bytes_uncompressed: int | None
    parts: int | None
    active_parts: int | None
    total_marks: int | None
    lifetime_rows: int | None
    lifetime_bytes: int | None
    comment: str
    has_own_data: int
    loading_dependencies_database: list[str]
    loading_dependencies_table: list[str]
    loading_dependent_database: list[str]
    loading_dependent_table: list[str]

class TablesQuery(BaseClickPyQuery[list[TableModel]]):
    QUERY: ClassVar
    databases: list[str]
