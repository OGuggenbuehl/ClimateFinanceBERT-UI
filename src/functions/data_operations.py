from typing import Optional

import pandas as pd


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


def subset_data_by_filters(
    df: pd.DataFrame,
    selected_categories: Optional[list[str]] = None,
    selected_subcategories: Optional[list[str]] = None,
    year_range: Optional[tuple[int, int]] = None,
) -> pd.DataFrame:
    """Subset the data based on the selected categories, subcategories, and year range."""
    df_subset = df

    # apply subcategory filter if provided
    if selected_subcategories:
        df_subset = df_subset[df_subset["climate_class"].isin(selected_subcategories)]

    # apply category filter if subcategories are not provided and categories exist
    elif selected_categories:
        df_subset = df_subset[df_subset["meta_category"].isin(selected_categories)]

    # apply year range filter if provided
    if year_range:
        df_subset = df_subset[df_subset["Year"].between(year_range[0], year_range[1])]

    return df_subset


def aggregate_to_country_level(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate data to the country level by summing USD_Disbursement."""
    return df.groupby("CountryCode")["USD_Disbursement"].sum().reset_index()


def merge_data(geojson: dict, df: pd.DataFrame) -> dict:
    """Merge the GeoJSON data with the DataFrame data to add the ClimFin-Data to each polygon."""
    merge_dict = pd.Series(
        df.USD_Disbursement.values, index=df["CountryCode"]
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

    return geojson


if __name__ == "__main__":
    import requests
    from components.constants import DUCKDB_PATH
    from functions.query_duckdb import construct_query, query_duckdb

    # retrieve geojson
    geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    response = requests.get(geojson_url)
    geojson_data = response.json()

    # query data
    selected_year = 2018
    query = construct_query(
        selected_year=selected_year,
        selected_categories=["Adaptation"],
        selected_subcategories=["Adaptation"],
        selected_donor_types=[
            "Donor Country"
        ],  # 'bilateral' as mapped in frontend component
    )
    df_queried = query_duckdb(
        duckdb_db=DUCKDB_PATH,
        query=query,
    )

    # aggregate to country level
    df_reshaped = reshape_by_type(df_queried, selected_type="donors")
    df_aggregated = aggregate_to_country_level(df_reshaped)
    print("aggregated data:")
    print(df_aggregated)

    # merge to geojson
    merged = merge_data(geojson_data, df_aggregated)
    print("\nmerged data as pulled from geojson:")
    for feature in merged["features"]:
        print(f'{feature["id"]}: {feature["properties"]["value"]}')
