import pandas as pd
from dash import Dash, dash_table

test_url = (
    "https://raw.githubusercontent.com/MalteToetzke/"
    "consistent-and-replicable-estimation-of-bilateral-climate-finance/"
    "main/Data/Recipients/recipients_2016.csv"
)


def render(app: Dash):
    data = pd.read_csv(test_url)
    table = dash_table.DataTable(
        data=data.to_dict("records"),
        columns=[{"name": i, "id": i} for i in data.columns],
    )
    return table
