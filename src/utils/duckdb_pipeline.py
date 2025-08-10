import logging
import os
import sys
import time

# add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.constants import DUCKDB_PATH, PARQUET_SOURCE, RAW_SOURCE, DataSources
from utils import duckdb_setup, parquet_converter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("duckdb_pipeline.log", mode="w"),
    ],
)
logger = logging.getLogger(__name__)


def main():
    """Run the DuckDB pipeline to set up a DuckDB database.

    The pipeline consists of two steps:
    1. Convert the CSV file to Parquet format.
    2. Set up a DuckDB database with the Parquet file as the data source.

    Parquet is used as an intermediary step to avoid memory overload when reading large CSV files and typing issues.
    """
    check_for_source_file()
    logger.info("Starting DuckDB pipeline...")
    start = time.time()

    logger.info("Converting CSV to Parquet...")
    parquet_converter.convert_csv_to_parquet(
        csv_file=RAW_SOURCE,
        parquet_file=PARQUET_SOURCE,
    )

    end = time.time()
    logger.info(f"CSV to Parquet conversion finished in {end - start:.2f} seconds.")

    logger.info("Setting up DuckDB database...")
    start = time.time()

    duckdb_setup.parquet_to_duckdb(
        parquet_path=PARQUET_SOURCE,
        db_path=DUCKDB_PATH,
    )

    end = time.time()
    logger.info(f"DuckDB setup finished in {end - start:.2f} seconds.")
    logger.info("DuckDB pipeline completed!")


def check_for_source_file():
    """Check if the source CSV file exists."""
    if not os.path.exists(RAW_SOURCE):
        logger.error(f"CSV file not found: {RAW_SOURCE}")
        logger.info(
            "If you want to use a different data source, modify the constants.py file."
        )
        logger.info(
            f"Development data source is set to: {DataSources.Development.RAW_SOURCE}"
        )
        logger.info(
            f"Production data source is set to: {DataSources.Production.RAW_SOURCE}"
        )
        raise FileNotFoundError(f"CSV file not found: {RAW_SOURCE}")


if __name__ == "__main__":
    main()
