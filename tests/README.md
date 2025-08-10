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

For coverage reporting:

```bash
python -m coverage run -m pytest ./tests
python -m coverage report
```

## Test Organization

- `conftest.py`: Common fixtures used across tests
- `test_app.py`: Tests for app initialization and configuration
- `test_components.py`: Tests for UI components
- `test_data_operations.py`: Tests for data transformation functions
- `test_query_duckdb.py`: Tests for DuckDB query functionality

## Adding New Tests

1. Create new test files with the prefix `test_` in the `tests/` directory
2. Use existing fixtures from `conftest.py` or create new ones
3. Follow the Arrange-Act-Assert pattern in your tests
4. Run tests to make sure they pass

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
- pytest-cov (for coverage)
- dash[testing] (for UI component testing)
