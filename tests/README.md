# ClimateFinanceBERT-UI Tests

This directory contains tests for the ClimateFinanceBERT-UI application. The tests are organized by functionality.

## Running Tests

You can run the tests using the Makefile command:

```bash
make test
```

Or directly with pytest:

```bash
python -m pytest ./tests
```

## Test Organization

- `conftest.py`: Common fixtures used across tests
- `test_app.py`: Tests for app initialization and configuration
- `test_components.py`: Tests for UI components
- `test_data_operations.py`: Tests for data transformation functions
- `test_query_duckdb.py`: Tests for DuckDB query functionality

## Test Coverage

The test suite aims to cover:

- Data processing functions
- UI component rendering
- Database query building
- Application configuration

## Mock Objects

Several mock objects are provided in `conftest.py` to simulate:
- DuckDB connections
- Sample finance data
- Application instances

## Dependencies

The test suite requires the following packages:
- pytest
- dash[testing] (for UI component testing)

These testing dependencies can be installed using `uv pip install -e ".[test]"`. 
This is done automatically when you run `make install`.
