# Copyright (C) 2021 Derek Lane, Cancer Care Associates
# Copyright (C) 2024 Simon Biggs

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import functools
from typing import cast

from pymedphys._imports import pandas as pd
from pymedphys._imports import sqlalchemy, toml

import pymedphys

from . import paths

MSQ_SERVER = "localhost"
MSQ_PORT = 1433

TEST_DB_NAME = "MosaiqTest77008"

SA_USER = "sa"
SA_PASSWORD = "sqlServerPassw0rd"


# Not knowing particularly why, I was unable to load values in as "char"
# or "timestamp". This is a work-a-round to just map those types to
# something else for now.
TYPE_CASTING = {
    "char": "varchar",
    "timestamp": "largebinary",
    "binary": "largebinary",
}


def connect(database=TEST_DB_NAME) -> pymedphys.mosaiq.Connection:
    connection = pymedphys.mosaiq.connect(
        MSQ_SERVER,
        port=MSQ_PORT,
        database=database,
        username=SA_USER,
        password=SA_PASSWORD,
    )

    return connection


@functools.lru_cache()
def load_csv_and_toml() -> tuple[dict[str, "pd.DataFrame"], dict[str, dict[str, str]]]:
    """Loads the *.csv files and types_map.toml file that are within
    this directory.
    """

    with open(paths.TYPES_MAP) as f:
        types_map = toml.load(f)

    for table, column_type_map in types_map.items():
        for column, type_repr in column_type_map.items():
            types_map[table][column] = _get_sql_type(type_repr)

    types_map = cast(dict[str, dict[str, str]], types_map)
    tables = _load_tables()

    sql_types_map = get_sqlalchemy_types_map()
    type_casting = {
        sql_types_map[key]: sql_types_map[item] for key, item in TYPE_CASTING.items()
    }

    for table_name, table in tables.items():
        for column_name, a_type in types_map[table_name].items():
            try:
                types_map[table_name][column_name] = type_casting[a_type]
            except KeyError:
                pass

    return tables, types_map


def _load_tables():
    csv_paths = paths.DATA.glob("*.csv")
    tables: dict[str, "pd.DataFrame"] = {}

    for path in csv_paths:
        table_name = path.stem
        tables[table_name] = pd.read_csv(
            path,
            index_col=0,
        )

    return tables


def _get_sql_type(sql_type: str):
    """Convert an SQL type labelled as a string to an SQLAlchemy type
    instance."""
    sql_type = str(sql_type).lower()
    sqlalchemy_types_map = get_sqlalchemy_types_map()

    return sqlalchemy_types_map[sql_type]


@functools.lru_cache()
def get_sqlalchemy_types_map():
    """Load up a map that converts string representations of SQLAlchemy
    types and maps them to their SQLAlchemy instance.
    """
    mssql_types = sqlalchemy.dialects.mssql
    mssql_types_map = _create_types_map(mssql_types)

    pymssql_types = sqlalchemy.dialects.mssql.pymssql.sqltypes
    pymssql_types_map = _create_types_map(pymssql_types)

    sqlalchemy_types_map = {
        **mssql_types_map,
        **pymssql_types_map,
    }
    return sqlalchemy_types_map


def _create_types_map(sql_types):
    """Take a types module and utilising the `dir` function create a
    mapping from the string value of that attribute to the SQLAlchemy
    type instance.
    """
    sql_types_map = {
        item.lower(): getattr(sql_types, item)
        for item in dir(sql_types)
        if item[0].isupper()
    }

    return sql_types_map
