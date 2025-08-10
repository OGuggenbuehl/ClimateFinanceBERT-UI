# DuckDB Pipeline

## Overview

The DuckDB pipeline is a data processing utility that converts the raw CSV data into a more efficient DuckDB database format used by the application for efficient querying. This pipeline is provided to quickly transform the raw source CSV data into the format expected by the application, enabling fast updating of source data. 

## Purpose

The pipeline serves several important purposes:

1. **Data Conversion**: Transforms raw CSV climate finance data into a DuckDB database format for better efficiency
2. **Data Update**: Allows for quick updates to the source data without needing to manually adjust the database
3. **Performance Optimization**: Reduces memory usage and improves query performance for the dashboard by providing the data in an optimized format

## Pipeline Process

The pipeline consists of two main steps:

1. **CSV to Parquet Conversion**:
   - Reads the raw CSV file using Polars for memory-efficient processing
   - Converts and stores data in Parquet columnar format
   - Maintains data types and structure

2. **Parquet to DuckDB**:
   - Creates a DuckDB database with the appropriate schema
   - Imports data from the Parquet file into the database
   - Applies optimizations for analytical queries

## Usage

### Running the Pipeline

```bash
# using the Makefile command (recommended)
make duckdb-pipeline

# or directly with Python
python src/utils/duckdb_pipeline.py
```

### Configuration

The pipeline uses configuration from `src/components/constants.py`:

- **Production Data**:
  - Raw CSV: `./data/all_crs_labelled.csv`
  - Parquet: `./data/ClimFinBERT_DB.parquet`
  - DuckDB: `./data/ClimFinBERT_DB.duckdb`

- **Development Data** (if using a smaller dataset for testing):
  - Raw CSV: `./data/sampled_df.csv`
  - Parquet: `./data/sampled_df.parquet`
  - DuckDB: `./data/db_small.duckdb`

To switch between production and development data sources, modify the imports in `constants.py`.

## Requirements

- Python 3.12+
- DuckDB
- Polars (for efficient CSV processing)
- Sufficient memory for processing large CSV files

## Logging

The pipeline logs detailed information about each step of the process:

- Progress indicators
- Timing information
- Error messages and diagnostics

Logs are written to both the console and `duckdb_pipeline.log` in the project root.

## Troubleshooting

### Common Issues

1. **Source file not found**:
   - Ensure the source CSV file exists at the expected location (default: `./data/all_crs_labelled.csv`)
   - Check the path configuration in `constants.py` under `DataSources`

2. **Memory errors**:
   - For large datasets, ensure your system has sufficient memory
   - Consider using a smaller development dataset for testing

3. **Database locked**:
   - Ensure no other processes are using the DuckDB database
   - Check that the application isn't running simultaneously

## Files

- `duckdb_pipeline.py`: Main pipeline orchestration
- `parquet_converter.py`: CSV to Parquet conversion utility
- `duckdb_setup.py`: DuckDB database creation and configuration
