import pandas as pd


def fetch_data(selected_type: str):
    """
    Fetch the data from Github depending on the type dropdown.
    """
    url_prefix = (
        "https://raw.githubusercontent.com/MalteToetzke"
        "/consistent-and-replicable-estimation-of-bilateral-"
        "climate-finance/main/Data"
    )
    if selected_type == "donors":
        data_url = url_prefix + "/Donors/donors.csv"

    else:
        data_url = url_prefix + "/Recipients/recipients.csv"

    return pd.read_csv(data_url)


def prepare_data_for_merge(df, selected_categories):
    """
    Prepare the data for merging with the GeoJSON data.
    """
    df_subset = df[df["climate_class"].isin(selected_categories)]
    df_aggregated = df_subset.groupby("country_code")["effective_funding"].sum().reset_index()
    return df_aggregated


def merge_data(geojson, df):
    merge_dict = pd.Series(df.effective_funding.values, index=df["country_code"]).to_dict()
    for feature in geojson["features"]:
        # Set the density value from the dataframe to the GeoJSON feature
        id = feature["id"]
        feature["properties"]["value"] = merge_dict.get(id, None)
    return geojson


if __name__ == "__main__":
    import requests

    # Retrieve GeoJSON data from URL
    geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    response = requests.get(geojson_url)
    geojson_data = response.json()

    # get df
    data = fetch_data(selected_type="recipients")
    df_subset = data[(data["climate_class"] == "Bioenergy") & (data["effective_year"] == 2012)]

    # Prepare data for merging
    df_prepared = prepare_data_for_merge(df_subset, selected_categories=["Bioenergy"])

    merged = merge_data(geojson_data, df_subset)
    for feature in merged["features"]:
        print(f'{feature["id"]}: {feature["properties"]["value"]}')
