from typing import Literal, Optional

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


def filter_data_by_donor_type(
    df: pd.DataFrame,
    donor_type: Literal["bilateral", "multilateral", "all"],
) -> pd.DataFrame:
    """Filter the data based on the donor type."""
    if donor_type not in ["bilateral", "multilateral", "all"]:
        raise ValueError(
            "Invalid donor type. Please select either 'bilateral', 'multilateral', or 'all'."
        )

    donor_type_map = {
        "bilateral": "Donor Country",
        "multilateral": "Multilateral Donor",
    }

    if donor_type in donor_type_map:
        return df[df["DonorType"] == donor_type_map[donor_type]]

    return df  # No filtering needed if donor_type is "all"


def prepare_data_for_merge(
    df: pd.DataFrame,
    selected_categories: Optional[list[str]] = None,
    selected_subcategories: Optional[list[str]] = None,
    year_range: Optional[tuple[int, int]] = None,
) -> pd.DataFrame:
    """Prepare the data for merging with the GeoJSON data."""
    # Filter the data according to inputs set in UI
    df_subset = subset_data_by_filters(
        df,
        selected_categories=selected_categories,
        selected_subcategories=selected_subcategories,
        year_range=year_range,
    )

    # Aggregate data to country level for display
    return aggregate_to_country_level(df_subset)


def subset_data_by_filters(
    df: pd.DataFrame,
    selected_categories: Optional[list[str]] = None,
    selected_subcategories: Optional[list[str]] = None,
    year_range: Optional[tuple[int, int]] = None,
) -> pd.DataFrame:
    """Subset the data based on the selected categories, subcategories, and year range."""
    df_subset = df

    # Apply subcategory filter if provided
    if selected_subcategories:
        df_subset = df_subset[df_subset["climate_class"].isin(selected_subcategories)]

    # Apply category filter if subcategories are not provided and categories exist
    elif selected_categories:
        df_subset = df_subset[df_subset["meta_category"].isin(selected_categories)]

    # Apply year range filter if provided
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

    # Filter out features whose ID is not in the merge_dict
    filtered_features = [
        feature for feature in geojson["features"] if feature["id"] in merge_dict
    ]

    # Update the properties of the remaining features
    for feature in filtered_features:
        id = feature["id"]
        feature["properties"]["value"] = merge_dict.get(id, 0)

    # Modify the GeoJSON to only include the filtered features
    geojson["features"] = filtered_features

    return geojson


if __name__ == "__main__":
    import requests
    from components.constants import DUCKDB_PATH
    from functions.query_duckdb import query_duckdb

    # Retrieve GeoJSON data from URL
    geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    response = requests.get(geojson_url)
    geojson_data = response.json()

    selected_years = (2014, 2020)
    query = f"""
            SELECT * FROM my_table
            WHERE Year >= {selected_years[0]} AND Year <= {selected_years[1]};
            """
    df_queried = query_duckdb(
        duckdb_db=DUCKDB_PATH,
        query=query,
    )
    df_type = reshape_by_type(df_queried, selected_type="donors")
    data = filter_data_by_donor_type(df_type, donor_type="bilateral")

    # Prepare data for merging
    df_prepared = prepare_data_for_merge(
        data,
        selected_categories=["Adaptation"],
        selected_subcategories=["Adaptation"],
        year_range=(2016, 2016),
    )
    print(df_prepared)

    merged = merge_data(geojson_data, df_prepared)
    for feature in merged["features"]:
        print(f'{feature["id"]}: {feature["properties"]["value"]}')
