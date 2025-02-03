from collections.abc import Iterable, Sequence
from typing import NamedTuple, TypeVar

import pandas as pd
import sqlalchemy as sa

from .. import utils

_T = TypeVar('_T', str, float)


class Metadata[_T](NamedTuple):
    table: sa.TableClause
    column: sa.ColumnClause[_T]
    cardinality: int
    sample_values: Sequence[_T]


def stringify(m: Metadata[_T]) -> str:
    is_sample = m.cardinality > len(m.sample_values)
    value_description = 'sample values' if is_sample else 'values'
    out = [
        f'column `{m.column.name}` of table `{m.table.name}` has cardinality of {m.cardinality}.',
        f'The following are the {value_description}: {m.sample_values}',
    ]
    return '\n'.join(out)


def generate_metadata(
    conn: sa.Connection, tbl: sa.TableClause
) -> Sequence[Metadata[_T]]:
    columns = _get_columns(conn, tbl)
    distinct_values = [
        Metadata(
            tbl,
            col,
            _get_distinct_count(conn, tbl, col),
            _retrieve_distinct_values(conn, tbl, col),
        )
        for col in columns
    ]
    return distinct_values


def _get_columns(
    conn: sa.Connection, tbl: sa.TableClause
) -> Sequence[sa.ColumnClause[_T]]:
    query = (
        sa.select(sa.column('column_name'), sa.column('data_type'))
        .select_from(sa.text('INFORMATION_SCHEMA.COLUMNS'))
        .where(sa.column('table_name') == tbl.name)
    )
    type_mapper = {
        'integer': sa.Integer,
        'tinyint': sa.SmallInteger,
        'smallint': sa.SmallInteger,
        'double': sa.Double,
        'bigint': sa.BigInteger,
        'numeric': sa.Numeric,
        'float': sa.Float,
        'varchar': sa.String,
        'text': sa.Text,
        'datetime': sa.DateTime,
        'date': sa.Date,
        'time': sa.Time,
        'boolean': sa.Boolean,
        'blob': sa.LargeBinary,
    }
    result = conn.execute(query)
    columns = [sa.column(col, type_mapper[_type.lower()]) for col, _type in result]
    return columns


def _retrieve_distinct_values[T: str | float](
    conn: sa.Connection,
    tbl: sa.TableClause,
    column: sa.ColumnClause[T],
    max_values: int = 20,
) -> Sequence[T]:
    query = _generate_distinct_value_query(tbl, column, max_values)
    result = conn.execute(query)
    values = [row[0] for row in result.fetchall()]
    return values


def _get_distinct_counts(
    conn: sa.Connection, tbl: sa.TableClause, columns: Iterable[sa.ColumnClause[_T]]
) -> pd.DataFrame:
    query = _generate_distinct_count_query(columns, tbl)
    result = conn.execute(query)
    df = utils.result_as_frame(result)
    return df


def _get_distinct_count(
    conn: sa.Connection, tbl: sa.TableClause, column: sa.ColumnClause[_T]
) -> int:
    query = _generate_distinct_count_query([column], tbl)
    result = conn.execute(query)
    return result.scalar_one()


def _generate_distinct_value_query[T](
    tbl: sa.TableClause, column: sa.ColumnClause[T], max_values: int
) -> sa.Select[tuple[T]]:
    query = sa.select(sa.distinct(column)).select_from(tbl).limit(max_values)
    return query


def _generate_distinct_count_query(
    columns: Iterable[sa.ColumnClause[_T]], tbl: sa.TableClause
) -> sa.Select[tuple[int, ...]]:
    return sa.select(
        *[sa.func.count(sa.distinct(c)).label(c.name) for c in columns]
    ).select_from(tbl)
