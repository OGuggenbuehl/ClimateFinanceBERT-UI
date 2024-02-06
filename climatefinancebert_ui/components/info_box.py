import pandas as pd
from dash import Dash, Input, Output, html

from climatefinancebert_ui.components import ids

test_url = (
    "https://raw.githubusercontent.com/MalteToetzke/"
    "consistent-and-replicable-estimation-of-bilateral-climate-finance/"
    "main/Data/Recipients/recipients_2016.csv"
)

TEST_DATA = pd.read_csv(test_url)


def render(app: Dash):
    @app.callback(
        Output(ids.INFO, "children"),
        Input(ids.COUNTRIES_LAYER, "clickData"),
    )
    def get_info(click_data=None):
        header = [html.H4("Country Selection")]
        if not click_data:
            return header + [html.P("Click a country")]
        return header + [
            html.B(click_data["properties"]["name"]),
            html.Br(),
            f"it's ID is: {click_data['id']}",
        ]

    # Create info control.
    info = html.Div(
        children=get_info(),
        id=ids.INFO,
        className="info",
        style={
            "position": "absolute",
            "top": "10px",
            "right": "10px",
            "zIndex": "1000",
        },
    )
    return info
