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
