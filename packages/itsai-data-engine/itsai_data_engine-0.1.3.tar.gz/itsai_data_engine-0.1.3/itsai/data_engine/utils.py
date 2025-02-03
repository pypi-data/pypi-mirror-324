from typing import TypeVar

import pandas as pd
import sqlalchemy as sa

_T = TypeVar('_T', str, float, bool)


def list_tables(conn: sa.Connection) -> pd.DataFrame:
    return result_as_frame(
        conn.execute(sa.text('SELECT * FROM INFORMATION_SCHEMA.TABLES'))
    )


def result_as_frame(result: sa.CursorResult[tuple[_T, ...]]) -> pd.DataFrame:
    return pd.DataFrame(result.fetchall(), columns=list(result.keys()))
