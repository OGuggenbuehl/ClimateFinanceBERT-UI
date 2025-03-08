import logging

import polars as pl
from components.constants import PARQUET_SOURCE, RAW_SOURCE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_csv_to_parquet(
    csv_file: str,
    parquet_file: str,
    separator: str = ",",
) -> None:
    """Convert a CSV file to Parquet format.

    Args:
        csv_file (str): The path to the CSV file
        parquet_file (str): The path to the resulting Parquet file
        separator (str, optional): The separator used in the CSV file. Defaults to ",".
    """
    logger.info(f"Converting {csv_file} to {parquet_file}...")
    df = pl.scan_csv(csv_file, separator=separator)

    df.sink_parquet(parquet_file)
    logger.info("Conversion completed successfully!")


if __name__ == "__main__":
    convert_csv_to_parquet(
        csv_file=RAW_SOURCE,
        parquet_file=PARQUET_SOURCE,
    )
