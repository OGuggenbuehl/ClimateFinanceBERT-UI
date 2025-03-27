import dash_bootstrap_components as dbc
from dash import Dash, html


def render(app: Dash) -> html.Div:
    return html.Div(
        id="download-page",
        children=[
            dbc.Col(
                [
                    html.H1("Download"),
                    # html.P("Find us on GitHub"),
                ],
                width={
                    "size": 6,
                    "offset": 3,
                },
            ),
        ],
    )
