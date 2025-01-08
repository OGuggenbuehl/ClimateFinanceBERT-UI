import dash_bootstrap_components as dbc
from dash import Dash, html


def render(app: Dash) -> html.Div:
    return html.Div(
        id="contact-page",
        children=[
            dbc.Col(
                [
                    html.H1("Contact"),
                    html.P("Find us on GitHub"),
                ],
                width={
                    "size": 6,
                    "offset": 3,
                },
            ),
        ],
    )
