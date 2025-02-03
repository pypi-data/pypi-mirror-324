import pathlib
from collections.abc import Sequence

import pandas as pd
import sqlalchemy as sa
import typer

from itsai.data_engine import utils
from itsai.data_engine.metadata import column


def main(db: pathlib.Path, outdir: pathlib.Path, type_: str = 'duckdb') -> None:
    engine = _DB_CONNECTORS[type_](db)
    with engine.connect() as conn:
        tables = utils.list_tables(conn)
        for tablename in tables['table_name']:
            table = sa.table(tablename)
            _process_table(table, conn, outdir.joinpath(f'{table.name}.xlsx'))


def _connect_to_duckdb(db: pathlib.Path) -> sa.Engine:
    engine = sa.create_engine(
        f'duckdb:///{db.as_posix()}', connect_args={'read_only': True}
    )
    return engine


def _process_table(
    table: sa.TableClause, conn: sa.Connection, outfile: pathlib.Path
) -> None:
    metadata = column.generate_metadata(conn, table)
    field_values = {}
    columns = []
    for col in metadata:
        columns.append(col.column.name)
        if col.cardinality <= len(col.sample_values):
            field_values[col.column.name] = col.sample_values

    with pd.ExcelWriter(outfile, engine='xlsxwriter') as writer:
        _create_metadata_table(columns, field='Columns').to_excel(
            writer, sheet_name='Columns', index=False
        )
        for key, values in field_values.items():
            _create_metadata_table(values, field='Category').to_excel(
                writer, sheet_name=key, index=False
            )


def _create_metadata_table(
    values: Sequence[str], field: str, description: str = 'Description'
) -> pd.DataFrame:
    return pd.DataFrame({field: values, description: len(values) * [None]})


_DB_CONNECTORS = {'duckdb': _connect_to_duckdb}

if __name__ == '__main__':
    typer.run(main)
