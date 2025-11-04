import logging
import time
from typing import Any, Literal, Optional

import pandas as pd
import requests

logger = logging.getLogger(__name__)


def reshape_by_type(
    df: pd.DataFrame,
    selected_type: Literal["donors", "recipients"],
) -> pd.DataFrame:
    """Reshape the dataframe based on whether we're viewing donors or recipients.

    Args:
        df: Input DataFrame with climate finance data
        selected_type: Either 'donors' or 'recipients'

    Returns:
        Reshaped DataFrame with standardized column names

    Raises:
        ValueError: If selected_type is not 'donors' or 'recipients'
    """
    reshape_config = {
        "donors": {
            "drop": ["DERecipientcode", "RecipientName"],
            "rename": {
                "DEDonorcode": "CountryCode",
                "DonorName": "CountryName",
            },
        },
        "recipients": {
            "drop": ["DEDonorcode", "DonorName"],
            "rename": {
                "DERecipientcode": "CountryCode",
                "RecipientName": "CountryName",
            },
        },
    }

    if selected_type not in reshape_config:
        raise ValueError(
            "Invalid selected type. Please select either 'donors' or 'recipients'."
        )

    config = reshape_config[selected_type]
    return df.drop(config["drop"], axis=1).rename(config["rename"], axis=1)


def create_mode_data(
    df: pd.DataFrame,
    map_mode: Literal["base", "total", "rio_oecd", "rio_climfinbert", "rio_diff"],
    selected_categories: Optional[list[str]] = None,
    selected_subcategories: Optional[list[str]] = None,
) -> pd.DataFrame:
    """Create the mode-specific DataFrame based on the selected visualization mode.

    Args:
        df: Input DataFrame as read from storage
        map_mode: Selected map visualization mode
        selected_categories: Selected climate finance categories
        selected_subcategories: Selected climate finance subcategories

    Returns:
        DataFrame for the selected mode, ready to be merged with GeoJSON data

    Raises:
        ValueError: If map_mode is not one of the supported modes
    """
    start_time = time.time()

    # Define mapping of modes to their data processing functions
    mode_functions = {
        "base": lambda: df,
        "total": lambda: aggregate(
            df=df,
            group_by=["Year", "CountryCode", "meta_category", "climate_class"],
            target="USD_Disbursement",
        ),
        "rio_oecd": lambda: build_oecd_table(
            df,
            selected_categories=selected_categories,
        ),
        "rio_climfinbert": lambda: build_ClimFinBERT_table(
            df,
            selected_categories=selected_categories,
            selected_subcategories=selected_subcategories,
        ),
        "rio_diff": lambda: build_difference_table(
            df,
            selected_categories=selected_categories,
        ),
    }

    if map_mode not in mode_functions:
        raise ValueError(
            f"Invalid map_mode: {map_mode}. Please select one of: {', '.join(mode_functions.keys())}"
        )

    # Execute the appropriate function for the selected mode
    result = mode_functions[map_mode]()

    # Log performance data
    end_time = time.time()
    logger.info(
        f"Execution time for creating data with mode {map_mode}: {end_time - start_time:.2f} seconds"
    )

    return result


def aggregate(
    df: pd.DataFrame,
    group_by: str | list[str] = "CountryCode",
    target: str = "USD_Disbursement",
) -> pd.DataFrame:
    """Aggregate data by grouping and summing the target variable.

    Args:
        df: Input DataFrame to aggregate
        group_by: Column or list of columns to group by
        target: Target column to sum

    Returns:
        Aggregated DataFrame
    """
    return df.groupby(group_by).agg({target: "sum"}).reset_index()


def merge_data(
    df: pd.DataFrame, geojson: dict[str, Any], map_mode: str
) -> dict[str, Any]:
    """Merge the GeoJSON data with the DataFrame data for map visualization.

    Args:
        df: DataFrame with climate finance data
        geojson: GeoJSON object with country polygons
        map_mode: Selected map visualization mode

    Returns:
        Enhanced GeoJSON with climate finance values
    """
    start = time.time()

    # For base mode, just return the original GeoJSON
    if map_mode == "base":
        return geojson

    # Create mapping dictionary based on the mode
    if map_mode in ["rio_oecd", "rio_climfinbert"]:
        # Aggregate by CountryCode to ensure unique values when multiple subcategories are selected
        agg_df = df.groupby("CountryCode")["USD_Disbursement"].sum().reset_index()
        merge_dict = pd.Series(
            agg_df.USD_Disbursement.values, index=agg_df["CountryCode"]
        ).to_dict()
    elif map_mode == "rio_diff":
        merge_dict = pd.Series(
            df.USD_Disbursement_diff.values, index=df["CountryCode"]
        ).to_dict()
    else:
        logger.warning(f"Unrecognized map_mode '{map_mode}' in merge_data")
        return geojson

    # Filter features to include only countries with data
    filtered_features = [
        feature for feature in geojson["features"] if feature["id"] in merge_dict
    ]

    # Add values to each feature's properties
    for feature in filtered_features:
        country_id = feature["id"]
        feature["properties"]["value"] = merge_dict.get(country_id, 0)

    # Update the geojson with filtered features
    geojson["features"] = filtered_features

    # Log performance data
    end = time.time()
    logger.info(f"Execution time for merging data: {end - start:.2f} seconds")

    return geojson


def build_oecd_table(
    df: pd.DataFrame,
    selected_categories: Optional[list[str]],
) -> pd.DataFrame:
    """Build a table based on OECD Rio markers.

    Args:
        df: Input DataFrame with climate finance data
        selected_categories: Categories to include in the table

    Returns:
        Filtered and aggregated DataFrame for OECD data
    """
    # Skip processing if no categories selected
    if not selected_categories:
        return df

    # Map UI category names to database column names
    categories_mapping = {
        "Mitigation": "ClimateMitigation",
        "Adaptation": "ClimateAdaptation",
        "Environment": "Biodiversity",
    }

    # Initialize filter condition
    filter_condition = pd.Series(False, index=df.index)

    # Build filter for selected categories
    for category in selected_categories:
        if category in categories_mapping:
            category_column = categories_mapping[category]
            # Handle NaN values to avoid breaking the condition
            filter_condition |= df[category_column].fillna(0) > 0

    # Apply the filter and aggregate data
    df_filtered = df[filter_condition]

    return aggregate(
        df_filtered,
        group_by=["Year", "CountryCode", "meta_category", "climate_class"],
        target="USD_Disbursement",
    )


def build_ClimFinBERT_table(
    df: pd.DataFrame,
    selected_categories: Optional[list[str]],
    selected_subcategories: Optional[list[str]] = None,
) -> pd.DataFrame:
    """Build a table based on ClimateFinanceBERT categorization.

    Args:
        df: Input DataFrame with climate finance data
        selected_categories: Categories to include
        selected_subcategories: Subcategories to include

    Returns:
        Filtered and aggregated DataFrame for ClimFinBERT data
    """
    # Apply category filter if categories are provided
    if selected_categories:
        df = df[df["meta_category"].isin(selected_categories)]

    # Apply subcategory filter if subcategories are provided
    if selected_subcategories:
        df = df[df["climate_class"].isin(selected_subcategories)]

    # Group and aggregate data based on the filters
    return aggregate(
        df,
        group_by=["Year", "CountryCode", "meta_category", "climate_class"],
        target="USD_Disbursement",
    )


def build_difference_table(
    df: pd.DataFrame,
    selected_categories: Optional[list[str]],
) -> pd.DataFrame:
    """Build a table showing the difference between OECD and ClimFinBERT categorization.

    Args:
        df: Input DataFrame with climate finance data
        selected_categories: Categories to include

    Returns:
        DataFrame with differences between OECD and ClimFinBERT data
    """
    oecd_df = build_oecd_table(
        df,
        selected_categories,
    )
    climfinbert_df = build_ClimFinBERT_table(
        df,
        selected_categories,
    )
    return calculate_difference(oecd_df, climfinbert_df)


def calculate_difference(
    oecd_df: pd.DataFrame,
    climfinbert_df: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate the difference between OECD and ClimFinBERT data.

    Args:
        oecd_df: DataFrame with OECD data
        climfinbert_df: DataFrame with ClimFinBERT data

    Returns:
        DataFrame with difference values
    """
    # Merge the dataframes on CountryCode
    diff_df = pd.merge(
        oecd_df,
        climfinbert_df,
        on=["CountryCode"],
        how="outer",
        suffixes=("_OECD", "_ClimFinBERT"),
    )

    # Replace NaN values with 0
    diff_df.fillna(0, inplace=True)

    # Calculate the difference between ClimFinBERT and OECD values
    diff_df["USD_Disbursement_diff"] = (
        diff_df["USD_Disbursement_ClimFinBERT"] - diff_df["USD_Disbursement_OECD"]
    )

    return diff_df


if __name__ == "__main__":
    """Test code for the data operations module."""
    from components.constants import DUCKDB_PATH
    from utils.query_duckdb import construct_country_summary_query, query_duckdb

    # Fetch GeoJSON data for testing
    geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    response = requests.get(geojson_url)
    geojson_data = response.json()

    # Query test data
    test_query = construct_country_summary_query(
        selected_year=2020,
        selected_categories=["Adaptation"],
        selected_subcategories=["Adaptation"],
        selected_donor_types=["Donor Country"],
        selected_flow_types=["ODA Loans", "ODA Grants"],
    )

    df_queried = query_duckdb(
        duckdb_db=DUCKDB_PATH,
        query=test_query,
    )

    # Test reshape operation
    df_reshaped = reshape_by_type(df_queried, selected_type="donors")

    # Test mode data creation
    df_prepared = create_mode_data(
        df_reshaped,
        map_mode="rio_oecd",
        selected_categories=["Adaptation"],
        selected_subcategories=["Adaptation"],
    )
    print("Prepared data:")
    print(df_prepared.head())

    # Test merge operation
    merged = merge_data(df=df_prepared, geojson=geojson_data, map_mode="rio_oecd")
    print("\nMerged data sample (first 3 countries):")
    for i, feature in enumerate(merged["features"][:3]):
        print(f"{feature['id']}: {feature['properties']['value']}")
