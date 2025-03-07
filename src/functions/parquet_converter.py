import logging

import polars as pl

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_csv_to_parquet(
    csv_file: str, parquet_file: str, separator: str = ","
) -> None:
    logger.info(f"Converting {csv_file} to {parquet_file}...")

    # Read CSV lazily to avoid memory overload
    df = pl.scan_csv(csv_file, separator=separator)

    # Save as Parquet format (efficient columnar storage)
    df.sink_parquet(parquet_file)

    logger.info("Conversion completed successfully!")


if __name__ == "__main__":
    convert_csv_to_parquet(
        csv_file="data/all_crs_labelled.csv",
        parquet_file="data/testing_large.parquet",
    )
