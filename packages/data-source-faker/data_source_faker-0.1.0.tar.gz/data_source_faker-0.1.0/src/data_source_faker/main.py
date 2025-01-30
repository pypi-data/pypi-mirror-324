import os
import time

import yaml
import schedule
import pandas as pd

from datetime import timedelta
from urllib.parse import urlparse
from faker import Faker
from typing import Union, List

from source_faker.logging.logging_mixin import LoggingMixin
from source_faker.models import DatabaseColumn, TableSettings, Config, ColumnType
from source_faker.providers import DatabaseColumnProvider
from source_faker.yaml.dumper import Dumper


class SourceFaker(LoggingMixin):

    def __init__(
        self,
        config_path: str = None,
        export_path: str = None
    ):
        self.config_path = config_path
        self.export_path = export_path
        self.tables: list[TableSettings] = []
        self.fake: Faker = self._faker_init()

        if config_path:
            config = self._parse_config(config_path)
            self.tables = config.tables

    def add_tables(self, tables: Union[TableSettings, List[TableSettings]]):
        if not isinstance(tables, list):
            tables = [tables]
        self.tables.extend(tables)

    def create_columns(self, col_amount: int) -> list[DatabaseColumn]:
        return [self.fake.database_column() for _ in range(1, col_amount + 1)]

    def run(self):
        self._validate()

        for table in self.tables:
            if not table.columns:
                table.columns = self.create_columns(col_amount=table.columns_amount)

            (schedule
             .every(table.batch_frequency_seconds)
             .seconds
             .until(timedelta(seconds=table.duration_seconds))
             .do(self._create_file, table))

        if self.export_path:
            self._export_config(
                config=Config(tables=self.tables),
                output_path=self.export_path
            )

        while True:
            schedule.run_pending()
            time.sleep(1)
            if not schedule.next_run():
                return

    def _validate(self):
        if not self.tables:
            raise ValueError(f"No tables defined, use the add_table method before running")

        # Create target directory if targeting the local file system
        for table in self.tables:
            url = urlparse(table.output_path)
            if not url.scheme and not os.path.exists(table.output_path):
                os.makedirs(table.output_path)

    @staticmethod
    def _parse_config(config_path: str) -> Config:
        with open(config_path, 'r') as file:
            raw_config = yaml.safe_load(file)

        if "tables" not in raw_config:
            raise ValueError("Root 'tables' key not found in config file provided")

        tables = []
        for table in raw_config['tables']:
            columns = []
            for column in table['columns']:
                columns.append(DatabaseColumn(
                    column_name=column['column_name'],
                    column_type=ColumnType(column['column_type'])
                ))

            tables.append(TableSettings(
                table_name=table['table_name'],
                output_path=table['output_path'],
                table_format=table['table_format'],
                columns=columns,
                duration_seconds=table.get('duration_seconds', TableSettings.duration_seconds),
                batch_frequency_seconds=table.get('batch_frequency_seconds', TableSettings.batch_frequency_seconds),
                batch_rows=table.get('batch_rows', TableSettings.batch_rows)
            ))

        return Config(tables=tables)

    @staticmethod
    def _export_config(config: Config, output_path: str):
        with open(output_path, 'w') as file:
            yaml.dump(
                data=config.to_dict(),
                stream=file,
                allow_unicode=True,
                sort_keys=False,
                canonical=False,
                encoding="utf-8",
                Dumper=Dumper
            )

    @staticmethod
    def _faker_init() -> Faker:
        fake = Faker(use_weighting=False)
        fake.add_provider(DatabaseColumnProvider)
        return fake

    def _create_file(self, table: TableSettings):
        current_timestamp = int(time.time())
        full_path = os.path.join(
            table.output_path,
            f"{table.table_name}_{current_timestamp}.parquet"
        )
        df = self._create_rows(table=table)
        df.to_parquet(full_path)

        self.log.info(f"Created file {full_path}")

    def _create_rows(self, table: TableSettings) -> pd.DataFrame:
        rows = []
        for i in range(1, table.batch_rows+1):
            row = {
                column.column_name: self._generate_column_value(column.column_type)
                for column in table.columns
            }
            rows.append(row)
        return pd.DataFrame(rows)

    def _generate_column_value(self, column_type: ColumnType):
        return {
            'boolean': self.fake.boolean,
            'date': self.fake.date,
            'float': self.fake.random_number,
            'integer': self.fake.random_int,
            'numeric':  self.fake.random_number,
            'serial': self.fake.random_int,
            'bigserial': self.fake.random_int,
            'uuid': self.fake.random_int,
            'text': self.fake.text,
            'timestamp': self.fake.unix_time,
            'varchar': self.fake.name
        }[column_type.value]()