import dash_bootstrap_components as dbc
from dash import html

from components import ids


def render():
    return html.Div(
        [
            html.Div(
                "Color Distribution:",
                style={"font-weight": "bold", "margin-bottom": "4px"},
            ),
            dbc.RadioItems(
                id=ids.COLOR_MODE,
                options=[
                    {"label": "Continuous", "value": "continuous"},
                    {"label": "Quartiles", "value": "quartile"},
                ],
                value="continuous",
                inline=True,
                className="map-control-radio",
                style={"font-size": "14px"},
            ),
        ],
    )
