import logging
import time
from typing import Literal, Optional

import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def reshape_by_type(
    df: pd.DataFrame,
    selected_type: str,
) -> pd.DataFrame:
    """Reshape the table based on the selected type."""
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
    """Create the mode DataFrame based on the selected mode.

    Args:
        df (pd.DataFrame): The input DataFrame as read from storage.
        map_mode (str): The selected map mode.
        selected_categories (Optional[list[str]], optional): The selected categories. Defaults to None.
        selected_subcategories (Optional[list[str]], optional): The selected subcategories. Defaults to None.

    Returns:
        pd.DataFrame: The mode DataFrame based on the selected mode. Ready to be merged with the GeoJSON data.
    """
    start_time = time.time()

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
            f"Invalid map_mode: {map_mode}. Please select a valid map mode."
        )

    result = mode_functions[map_mode]()
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
    """Aggregate data to the country level by summing the target variable (default USD_Disbursement)."""
    return df.groupby(group_by).agg({target: "sum"}).reset_index()


def merge_data(df: pd.DataFrame, geojson: dict, map_mode: str) -> dict:
    """Merge the GeoJSON data with the DataFrame data to add the ClimFin-Data to each polygon."""
    start = time.time()
    if map_mode == "base":
        return geojson
    elif map_mode in ["rio_oecd", "rio_climfinbert"]:
        merge_dict = pd.Series(
            df.USD_Disbursement.values, index=df["CountryCode"]
        ).to_dict()
    elif map_mode == "rio_diff":
        merge_dict = pd.Series(
            df.USD_Disbursement_diff.values, index=df["CountryCode"]
        ).to_dict()

    # filter out features whose ID is not in the merge_dict
    # NOTE: this prevents buggy polygon coloring behavior
    filtered_features = [
        feature for feature in geojson["features"] if feature["id"] in merge_dict
    ]

    # merge the values to the remaining features
    for feature in filtered_features:
        id = feature["id"]
        feature["properties"]["value"] = merge_dict.get(id, 0)

    # subset geojson to only include the remaining features
    geojson["features"] = filtered_features

    end = time.time()
    logger.info(f"Execution time for merging data: {end - start:.2f} seconds")
    return geojson


def build_oecd_table(
    df: pd.DataFrame,
    selected_categories: Optional[list[str]],
) -> pd.DataFrame:
    """
    Build the OECD table based on the selected type, year range, and selected categories.
    Args:
        df (pd.DataFrame): The input DataFrame as read from the global variable.
        selected_categories (list): A list of selected categories to filter the data.

    Returns:
        pd.DataFrame: The OECD table based on the selected type, year range, and selected categories, aggregated to the country level.
    """

    # Handle multiple selected categories
    categories_mapping = {
        "Mitigation": "ClimateMitigation",
        "Adaptation": "ClimateAdaptation",
        "Environment": "Biodiversity",
    }

    # Initialize the filter condition to True (ensure the Series has the same index as df)
    filter_condition = pd.Series(True, index=df.index)

    # TODO: this needs bugfixing as not all polygons are colored as expected (check 2018, recipients, private and play with categories)
    for category in selected_categories:
        if category in categories_mapping:
            category_column = categories_mapping[category]
            # Handle NaN values by using .fillna(False) so that NaN values don't break the condition
            filter_condition |= df[category_column].fillna(0) > 0

    # Apply the filter condition to the dataframe
    df = df[filter_condition]

    # Aggregate data to country level by summing USD_Disbursement
    df = aggregate(
        df,
        group_by=["Year", "CountryCode", "meta_category", "climate_class"],
        target="USD_Disbursement",
    )

    return df


def build_ClimFinBERT_table(
    df: pd.DataFrame,
    selected_categories: Optional[list[str]],
    selected_subcategories: Optional[list[str]] = None,
) -> pd.DataFrame:
    """Build the ClimFinBERT table based on the selected type, year range, selected categories, and selected subcategories.

    Args:
        df (pd.DataFrame): The input DataFrame as read from the global variable.
        selected_categories (list[str], optional): A list of selected categories to filter the data.
        selected_subcategories (list[str], optional): A list of selected subcategories to filter the data. Defaults to None.

    Returns:
        pd.DataFrame: The ClimFinBERT table based on the selected type, year range, selected categories, and selected subcategories, aggregated to the country level.
    """

    # Apply category filter if categories are provided
    if selected_categories:
        df = df[df["meta_category"].isin(selected_categories)]

    # Apply subcategory filter if subcategories are provided
    if selected_subcategories:
        df = df[df["climate_class"].isin(selected_subcategories)]

    # Group and aggregate data based on the filters
    df = aggregate(
        df,
        group_by=["Year", "CountryCode", "meta_category", "climate_class"],
        target="USD_Disbursement",
    )

    return df


def build_difference_table(
    df: pd.DataFrame,
    selected_categories: Optional[list[str]],
) -> pd.DataFrame:
    """Build the difference table based on the selected type, year range, and selected categories.

    Args:
        df (pd.DataFrame): The input DataFrame as read from the global variable.
        selected_categories (list[str], optional): A list of selected categories to filter the data.

    Returns:
        pd.DataFrame: The difference table based on the selected type, year range, and selected categories, aggregated to the country level.
    """
    oecd_df = build_oecd_table(
        df,
        selected_categories,
    )
    ClimFinBERT_df = build_ClimFinBERT_table(
        df,
        selected_categories,
    )
    diff_df = calculate_difference(oecd_df, ClimFinBERT_df)
    return diff_df


def calculate_difference(
    oecd_df: pd.DataFrame,
    ClimFinBERT_df: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate the difference between the OECD and ClimFinBERT data.

    Args:
        oecd_df (pd.DataFrame): The OECD DataFrame.
        ClimFinBERT_df (pd.DataFrame): The ClimFinBERT DataFrame.

    Returns:
        pd.DataFrame: The difference DataFrame between the OECD and ClimFinBERT data.
    """
    diff_df = pd.merge(
        oecd_df,
        ClimFinBERT_df,
        on=["CountryCode"],
        how="outer",
        suffixes=("_OECD", "_ClimFinBERT"),
    )
    diff_df.fillna(0, inplace=True)
    diff_df["USD_Disbursement_diff"] = (
        diff_df["USD_Disbursement_ClimFinBERT"] - diff_df["USD_Disbursement_OECD"]
    )
    return diff_df


if __name__ == "__main__":
    import requests

    from components.constants import DUCKDB_PATH
    from functions.query_duckdb import construct_query, query_duckdb

    # retrieve geojson
    geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    response = requests.get(geojson_url)
    geojson_data = response.json()

    # query data
    query = construct_query(
        year_type="single_year",
        selected_year=2020,
        selected_categories=["Adaptation"],
        selected_subcategories=["Adaptation"],
        selected_donor_types=[
            "Donor Country"
        ],  # 'bilateral' as mapped in frontend component
        selected_flow_types=["ODA Loans", "ODA Grants"],
    )
    df_queried = query_duckdb(
        duckdb_db=DUCKDB_PATH,
        query=query,
    )
    # aggregate to country level and rename donor / recipient columns
    df_reshaped = reshape_by_type(df_queried, selected_type="donors")

    # prepare data for chosen mode
    df_prepared = create_mode_data(
        df_reshaped,
        map_mode="rio_oecd",
        selected_categories=["Adaptation"],
        selected_subcategories=["Adaptation"],
    )
    print("prepared data:")
    print(df_prepared)

    # merge to geojson
    merged = merge_data(df=df_prepared, geojson=geojson_data, map_mode="rio_oecd")
    print("\nmerged data as pulled from geojson:")
    for feature in merged["features"]:
        print(f"{feature['id']}: {feature['properties']['value']}")
