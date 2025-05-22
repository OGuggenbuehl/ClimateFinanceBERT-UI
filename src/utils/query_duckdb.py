import logging
import time
from typing import Literal, Optional, Tuple

import duckdb
import pandas as pd

from components.widgets.donor_type import DONOR_TYPE_MAP

logger = logging.getLogger(__name__)


def ensure_list(value: Optional[str | list[str]]) -> list[str]:
    """Convert a single value or list to a list, handling None values.

    Args:
        value: String, list of strings, or None

    Returns:
        Normalized list, empty if input was None
    """
    if not value:
        return []
    return [value] if isinstance(value, str) else value


def format_value_list(values: list[str]) -> str:
    """Format a list of values for inclusion in SQL query.

    Args:
        values: List of string values

    Returns:
        Comma-separated string of quoted values
    """
    return ", ".join(f"'{val}'" for val in values)


def validate_donor_types(selected_donor_types: list[str]) -> None:
    """Validate that selected donor types are valid.

    Args:
        selected_donor_types: List of donor types to validate

    Raises:
        ValueError: If any donor type is invalid
    """
    invalid_donor_types = [
        dt for dt in selected_donor_types if dt not in DONOR_TYPE_MAP.values()
    ]

    if invalid_donor_types:
        allowed_values = ", ".join(f"'{val}'" for val in DONOR_TYPE_MAP.values())
        raise ValueError(
            f"Invalid donor types selected: {invalid_donor_types}. Only {allowed_values} are allowed."
        )


def add_year_filter(
    query: str, year_type: str, selected_year: int | Tuple[int, int]
) -> str:
    """Add year filter clause to a query.

    Args:
        query: Base SQL query
        year_type: Type of year filter ('single_year' or 'timespan')
        selected_year: Year value or range tuple

    Returns:
        Query with year filter added
    """
    if year_type == "single_year":
        return query + f"\nWHERE Year = {selected_year}\n"
    elif year_type == "timespan":
        return (
            query
            + f"\nWHERE Year >= {selected_year[0]} AND Year <= {selected_year[1]}\n"
        )
    else:
        raise ValueError(f"Invalid year_type: {year_type}")


def add_category_filter(query: str, categories: list[str]) -> str:
    """Add category filter to a query.

    Args:
        query: SQL query to modify
        categories: List of categories to filter by

    Returns:
        Query with category filter added
    """
    if not categories:
        return query

    category_list = format_value_list(categories)
    return query + f" AND meta_category IN ({category_list})"


def add_subcategory_filter(query: str, subcategories: list[str]) -> str:
    """Add subcategory filter to a query.

    Args:
        query: SQL query to modify
        subcategories: List of subcategories to filter by

    Returns:
        Query with subcategory filter added
    """
    if not subcategories:
        return query

    subcategory_list = format_value_list(subcategories)
    return query + f" AND climate_class IN ({subcategory_list})"


def add_flow_type_filter(query: str, flow_types: list[str]) -> str:
    """Add flow type filter to a query.

    Args:
        query: SQL query to modify
        flow_types: List of flow types to filter by

    Returns:
        Query with flow type filter added
    """
    if not flow_types:
        return query

    flow_type_list = format_value_list(flow_types)
    return query + f" AND FlowName IN ({flow_type_list})"


def add_donor_type_filter(query: str, donor_types: list[str]) -> str:
    """Add donor type filter to a query.

    Args:
        query: SQL query to modify
        donor_types: List of donor types to filter by

    Returns:
        Query with donor type filter added

    Raises:
        ValueError: If any donor type is invalid
    """
    if not donor_types:
        return query

    # Validate donor types
    validate_donor_types(donor_types)

    # Add appropriate IN or = clause based on number of donor types
    if len(donor_types) > 1:
        return query + f" AND DonorType IN {tuple(donor_types)}"
    else:
        return query + f" AND DonorType = '{donor_types[0]}'"


def construct_query(
    year_type: Literal["single_year", "timespan"],
    selected_year: int | Tuple[int, int],
    selected_categories: Optional[str | list[str]] = None,
    selected_subcategories: Optional[str | list[str]] = None,
    selected_donor_types: Optional[str | list[str]] = None,
    selected_flow_types: Optional[str | list[str]] = None,
) -> str:
    """Construct an SQL query based on the selected filters.

    Args:
        year_type: Type of year filter to apply ('single_year' or 'timespan')
        selected_year: Selected year or range tuple
        selected_categories: Categories to filter by
        selected_subcategories: Subcategories to filter by
        selected_donor_types: Donor types to filter by
        selected_flow_types: Flow types to filter by

    Returns:
        Complete SQL query string

    Raises:
        ValueError: If year_type is invalid or donor types are invalid
    """
    # Start with base query
    query = "SELECT *\nFROM my_table"

    # Add year filter
    query = add_year_filter(query, year_type, selected_year)

    # Normalize all filter inputs to lists
    categories = ensure_list(selected_categories)
    subcategories = ensure_list(selected_subcategories)
    donor_types = ensure_list(selected_donor_types)
    flow_types = ensure_list(selected_flow_types)

    # Add remaining filters
    query = add_category_filter(query, categories)
    query = add_subcategory_filter(query, subcategories)
    query = add_flow_type_filter(query, flow_types)
    query = add_donor_type_filter(query, donor_types)

    return query


def construct_aggregated_query(
    selected_year: int,
    selected_categories: Optional[str | list[str]] = None,
    selected_subcategories: Optional[str | list[str]] = None,
    selected_donor_types: Optional[str | list[str]] = None,
    selected_flow_types: Optional[str | list[str]] = None,
) -> str:
    """Construct an aggregated SQL query based on the selected filters.

    Args:
        selected_year: Year to filter by
        selected_categories: Categories to filter by
        selected_subcategories: Subcategories to filter by
        selected_donor_types: Donor types to filter by
        selected_flow_types: Flow types to filter by

    Returns:
        Complete SQL query string with aggregation

    Raises:
        ValueError: If donor types are invalid
    """
    # Start with base aggregation query
    query = """
        SELECT Year, DonorName, DEDonorcode, RecipientName, DERecipientcode, 
               FlowName, meta_category, climate_class, 
               SUM(USD_Disbursement) AS total_disbursement
        FROM my_table
    """

    # Add year filter
    query += f"WHERE Year = {selected_year}"

    # Normalize all filter inputs to lists
    categories = ensure_list(selected_categories)
    subcategories = ensure_list(selected_subcategories)
    donor_types = ensure_list(selected_donor_types)
    flow_types = ensure_list(selected_flow_types)

    # Add remaining filters
    query = add_category_filter(query, categories)
    query = add_subcategory_filter(query, subcategories)
    query = add_flow_type_filter(query, flow_types)
    query = add_donor_type_filter(query, donor_types)

    # Add grouping and ordering
    query += """
        GROUP BY DonorName, DEDonorcode, RecipientName, DERecipientcode, Year, 
                 FlowName, meta_category, climate_class
        ORDER BY total_disbursement DESC
    """

    return query


def query_duckdb(
    duckdb_db: str,
    query: str,
) -> pd.DataFrame:
    """Execute a query against a DuckDB database.

    Args:
        duckdb_db: Path to the DuckDB database file
        query: SQL query to execute

    Returns:
        DataFrame with query results
    """
    logger.info(f"Executing query on {duckdb_db}...")
    start = time.time()

    # Connect to database, execute query, and close connection
    con = duckdb.connect(database=duckdb_db)
    result_df = con.execute(query).fetchdf()
    con.close()

    # Log performance data
    end = time.time()
    logger.info(f"Query executed in {end - start:.2f} seconds")

    return result_df


if __name__ == "__main__":
    """Test code for query functions."""
    from components.constants import DUCKDB_PATH

    # Example of aggregated query
    test_query = construct_aggregated_query(
        selected_year=2018,
        selected_categories=["Adaptation"],
        selected_subcategories=["Adaptation"],
        selected_donor_types=["Donor Country"],
        selected_flow_types=["ODA Grants"],
    )

    print("Constructed query:")
    print(test_query)

    # Execute the query
    result = query_duckdb(duckdb_db=DUCKDB_PATH, query=test_query)

    # Display results
    print(f"Resulting dataframe has dimensions: {result.shape}")
    print(result.head())
    print(result.columns)
