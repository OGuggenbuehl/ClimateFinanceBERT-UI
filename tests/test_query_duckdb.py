"""Tests for DuckDB query functionality."""

import pytest

from components.widgets.donor_type import DONOR_TYPE_MAP
from utils.query_duckdb import ensure_list, format_value_list, validate_donor_types


def test_ensure_list_none():
    """Test ensure_list with None input."""
    assert ensure_list(None) == []


def test_ensure_list_string():
    """Test ensure_list with string input."""
    assert ensure_list("test") == ["test"]


def test_ensure_list_already_list():
    """Test ensure_list with list input."""
    assert ensure_list(["test1", "test2"]) == ["test1", "test2"]


def test_format_value_list():
    """Test format_value_list function."""
    values = ["value1", "value2", "value3"]
    result = format_value_list(values)
    assert result == "'value1', 'value2', 'value3'"


def test_validate_donor_types_valid():
    """Test validate_donor_types with valid types."""
    valid_types = list(DONOR_TYPE_MAP.values())[:2]  # first two valid types
    validate_donor_types(valid_types)


def test_validate_donor_types_invalid():
    """Test validate_donor_types with invalid types."""
    with pytest.raises(ValueError):
        validate_donor_types(["invalid_type"])


def test_query_duckdb_connection(mock_duckdb_conn):
    """Test DuckDB connection and query execution."""
    from utils.query_duckdb import query_duckdb

    result_df = query_duckdb("dummy.duckdb", "SELECT * FROM dummy")

    assert len(result_df) > 0
    assert "DEDonorcode" in result_df.columns
    assert "DonorName" in result_df.columns
