import logging
import time

import duckdb
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def query_duckdb_with_duckdb(
    duckdb_db: str,
    query: str,
) -> pd.DataFrame:
    """Query a DuckDB database.

    Args:
        duckdb_db (str): The path to the DuckDB database file
        query (str): The SQL query to execute

    Returns:
        pd.DataFrame: The resulting DataFrame
    """
    logger.info(f"Executing query on {duckdb_db}...")
    start = time.time()

    con = duckdb.connect(database=duckdb_db)
    formatted_query = query.format(duckdb_db=duckdb_db)
    result_df = con.execute(formatted_query).fetchdf()
    con.close()

    end = time.time()
    logger.info(f"Query executed in {end - start:.2f} seconds")
    return result_df


if __name__ == "__main__":
    from components.constants import DUCKDB_PATH

    query = "SELECT * FROM my_table WHERE DEDonorcode = 'GBR' AND Year >= 2018;"

    result = query_duckdb_with_duckdb(duckdb_db=DUCKDB_PATH, query=query)
    print(f"Resulting dataframe has dimensions: {result.shape}")
    print(result.head())
