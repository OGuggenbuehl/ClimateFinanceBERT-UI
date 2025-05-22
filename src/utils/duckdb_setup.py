import logging

import duckdb

from components.constants import COLUMN_TYPES

logger = logging.getLogger(__name__)


def parquet_to_duckdb(parquet_path: str, db_path: str, table_name: str = "my_table"):
    logger.info(f"Converting {parquet_path} to {db_path}...")

    con = duckdb.connect(db_path)

    # create the table with the specified schema
    columns_sql = ", ".join([f"{col} {dtype}" for col, dtype in COLUMN_TYPES.items()])
    con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})")

    # load only the specified columns from Parquet
    columns_str = ", ".join(COLUMN_TYPES.keys())

    con.execute(f"""
        INSERT INTO {table_name} ({columns_str})
        SELECT {columns_str} 
        FROM read_parquet('{parquet_path}')
    """)

    con.close()
    logger.info(f"Parquet successfully converted and stored in {db_path}.")


if __name__ == "__main__":
    from components.constants import DUCKDB_PATH, PARQUET_SOURCE

    parquet_to_duckdb(
        parquet_path=PARQUET_SOURCE,
        db_path=DUCKDB_PATH,
    )
