import logging
import time

import duckdb
import pandas as pd

logger = logging.getLogger(__name__)


def query_parquet_with_duckdb(
    parquet_db: str,
    query: str,
) -> pd.DataFrame:
    """Query a Parquet database using DuckDB.

    Args:
        parquet_db (str): The path to the Parquet database
        query (str): The SQL query to execute

    Returns:
        pd.DataFrame: The resulting DataFrame
    """
    logger.info(f"Executing query on {parquet_db}...")
    start = time.time()

    con = duckdb.connect(database=":memory:")
    formatted_query = query.format(parquet_db=parquet_db)
    result_df = con.execute(formatted_query).fetchdf()

    end = time.time()
    logger.info(f"Query executed in {end - start:.2f} seconds")
    return result_df


if __name__ == "__main__":
    from components.constants import COLUMN_TYPES, PARQUET_SOURCE

    columns_str = ", ".join(COLUMN_TYPES.keys())

    query = f"SELECT {columns_str} FROM parquet_scan('{{parquet_db}}') WHERE DEDonorcode = 'GBR' AND Year >= 2018;"

    result = query_parquet_with_duckdb(parquet_db=PARQUET_SOURCE, query=query)
    print(f"Resulting dataframe has dimensions: {result.shape}")
    print(result.head())
