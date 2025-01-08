import dash_bootstrap_components as dbc
from dash import Dash, html


def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            dbc.Col(
                [
                    html.H1("About"),
                    html.P("This is a simple web app to visualize data on a map."),
                    html.P(
                        "This app is built using Dash and Dash Bootstrap Components."
                    ),
                    html.P("The data is stored in a GeoJSON file."),
                    html.P("The map is rendered using Mapbox."),
                    html.P("The data is visualized using Plotly."),
                    html.P("The source code for this app can be found on GitHub."),
                ],
                width={
                    "size": 6,
                    "offset": 3,
                },
            ),
        ]
    )
