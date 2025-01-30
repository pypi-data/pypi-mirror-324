from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Literal

class ColumnType(Enum):
    BOOLEAN='boolean'
    DATE='date'
    FLOAT='float'
    INTEGER='integer'
    NUMERIC='numeric'
    SERIAL='serial'
    BIGSERIAL='bigserial'
    UUID='uuid'
    TEXT='text'
    TIMESTAMP='timestamp'
    VARCHAR='varchar'

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(node._value_)


@dataclass
class DatabaseColumn:
    column_name: str
    column_type: ColumnType

@dataclass
class TableSettings:
    table_name: str
    output_path: str
    table_format: Literal['parquet', 'csv', 'json', 'text']
    columns: list[DatabaseColumn] = field(default_factory=lambda: [])
    columns_amount: int = 10  # if columns are not set, generate columns based on this param
    batch_frequency_seconds: int = 10
    duration_seconds: int = 60
    batch_rows: int = 100

@dataclass
class Config:
    tables: list[TableSettings]
    to_dict = asdict
