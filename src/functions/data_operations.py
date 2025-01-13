from typing import Literal, Optional

import pandas as pd
import polars as pl


def read_data(
    selected_type: Literal["donors", "recipients"],
    source: str,
    columns: list,
    donor_type: Literal["bilateral", "multilateral", "all"] = "bilateral",
) -> pd.DataFrame:
    """Read the data from the source and return the data based on the selected type and donor type.

    Args:
        selected_type (Literal["donors", "recipients"]): Whether to return the donors or recipients
        source (str): The path to the source file
        columns (list): The columns to read from the source
        donor_type (Literal["bilateral", "multilateral", "all"]): The type of donor to filter the data. Defaults to "bilateral".

    Returns:
        pl.DataFrame: The data based on the selected type and donor type
    """
    df = pl.read_csv(source=source, columns=columns)

    data = reshape_by_type(df, selected_type)

    data = filter_data_by_donor_type(data, donor_type)

    return data.to_pandas()


def reshape_by_type(df: pl.DataFrame, selected_type: str) -> pl.DataFrame:
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

    # Validate the selected type
    if selected_type not in reshape_config:
        raise ValueError(
            "Invalid selected type. Please select either 'donors' or 'recipients'."
        )

    # Apply the reshaping logic based on the selected type
    config = reshape_config[selected_type]
    return df.drop(config["drop"]).rename(config["rename"])


def filter_data_by_donor_type(
    df: pl.DataFrame, donor_type: Literal["bilateral", "multilateral", "all"]
) -> pl.DataFrame:
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
        return df.filter(df["DonorType"] == donor_type_map[donor_type])

    return df  # No filtering needed if donor_type is "all"


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
    """
    Aggregate data to the country level by summing USD_Disbursement.
    """
    return df.groupby("CountryCode")["USD_Disbursement"].sum().reset_index()


def prepare_data_for_merge(
    df: pd.DataFrame,
    selected_categories: Optional[list[str]] = None,
    selected_subcategories: Optional[list[str]] = None,
    year_range: Optional[tuple[int, int]] = None,
) -> pd.DataFrame:
    """
    Prepare the data for merging with the GeoJSON data.
    """
    # Filter the data
    df_subset = subset_data_by_filters(
        df, selected_categories, selected_subcategories, year_range
    )

    # Aggregate data to country level
    return aggregate_to_country_level(df_subset)


def merge_data(geojson: dict, df: pd.DataFrame) -> dict:
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

    # Retrieve GeoJSON data from URL
    geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    response = requests.get(geojson_url)
    geojson_data = response.json()

    # read sample df
    import pandas as pd
    import polars as pl
    from components.constants import COLS, SOURCE

    data = read_data(
        selected_type="donors",
        source=SOURCE,
        columns=COLS,
        donor_type="bilateral",
    )

    # Prepare data for merging
    df_prepared = prepare_data_for_merge(
        data,
        selected_categories=["Adaptation"],
        selected_subcategories=["Adaptation"],
        year_range=(2012, 2012),
    )
    print(df_prepared)

    merged = merge_data(geojson_data, df_prepared)
    for feature in merged["features"]:
        print(f'{feature["id"]}: {feature["properties"]["value"]}')
