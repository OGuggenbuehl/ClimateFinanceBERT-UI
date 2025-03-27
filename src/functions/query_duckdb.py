import logging
import time
from typing import Optional, Union

import duckdb
import pandas as pd

from components.donor_type_dropdown import DONOR_TYPE_MAP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def construct_query(
    selected_year: int,
    selected_categories: Optional[Union[str, list[str]]] = None,
    selected_subcategories: Optional[Union[str, list[str]]] = None,
    selected_donor_types: Optional[Union[str, list[str]]] = None,
    selected_flow_types: Optional[Union[str, list[str]]] = None,
) -> str:
    """Construct an SQL query based on the selected filters.

    Args:
        selected_year (int): The selected year.
        selected_categories (Optional[Union[str, list[str]]]): The selected categories.
        selected_subcategories (Optional[Union[str, list[str]]]): The selected subcategories.
        selected_donor_types (Optional[Union[str, list[str]]]): The selected donor types.
        selected_flow_types (Optional[Union[str, list[str]]]): The selected flow types.

    Returns:
        str: The constructed SQL query.
    """
    # base query
    query = f"""
        SELECT *
        FROM my_table
        WHERE Year = {selected_year}
        """

    # normalize inputs to lists
    def ensure_list(value: Optional[Union[str, list[str]]]) -> list[str]:
        if not value:
            return []
        return [value] if isinstance(value, str) else value

    selected_categories = ensure_list(selected_categories)
    selected_subcategories = ensure_list(selected_subcategories)
    selected_donor_types = ensure_list(selected_donor_types)

    # add category filter
    if selected_categories:
        category_list = ", ".join(f"'{cat}'" for cat in selected_categories)
        query += f" AND meta_category IN ({category_list})"

    # add subcategory filter
    if selected_subcategories:
        subcategory_list = ", ".join(f"'{sub}'" for sub in selected_subcategories)
        query += f" AND climate_class IN ({subcategory_list})"

    # add flow type filter
    if selected_flow_types:
        flow_type_list = ", ".join(f"'{flow}'" for flow in selected_flow_types)
        query += f" AND FlowName IN ({flow_type_list})"

    # add donor type filter
    if selected_donor_types:
        # validate  selected donor types
        invalid_donor_types = [
            dt for dt in selected_donor_types if dt not in DONOR_TYPE_MAP.values()
        ]
        if invalid_donor_types:
            allowed_values = ", ".join(f"'{val}'" for val in DONOR_TYPE_MAP.values())
            raise ValueError(
                f"Invalid donor types selected: {invalid_donor_types}. Only {allowed_values} are allowed."
            )

        query += f" AND DonorType {'IN' if len(selected_donor_types) > 1 else '='} {tuple(selected_donor_types) if len(selected_donor_types) > 1 else repr(selected_donor_types[0])}"

    return query


def query_duckdb(
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
    # formatted_query = query.format(duckdb_db=duckdb_db)
    result_df = con.execute(query).fetchdf()
    con.close()

    end = time.time()
    logger.info(f"Query executed in {end - start:.2f} seconds")
    return result_df


if __name__ == "__main__":
    from components.constants import DUCKDB_PATH

    query = construct_query(
        selected_year=2018,
        selected_categories=["Adaptation"],
        selected_subcategories=["Adaptation"],
        selected_donor_types=["Donor Country"],
    )

    print("Constructed query:")
    print(query)

    result = query_duckdb(duckdb_db=DUCKDB_PATH, query=query)
    print(f"Resulting dataframe has dimensions: {result.shape}")
    print(result.head())
