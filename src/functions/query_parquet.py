import logging

import duckdb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def query_parquet_with_duckdb(parquet_db: str, query: str):
    logger.info(f"Executing query on {parquet_db}...")

    con = duckdb.connect(database=":memory:")

    formatted_query = query.format(parquet_db=parquet_db)
    result_df = con.execute(formatted_query).fetchdf()

    logger.info("Query execution completed.")

    return result_df


if __name__ == "__main__":
    db_path = "./data/testing_large.parquet"
    query = "SELECT * FROM parquet_scan('{parquet_db}') WHERE DEDonorcode = 'GBR' AND Year >= 2018;"

    result = query_parquet_with_duckdb(parquet_db=db_path, query=query)

    print(result.head())
