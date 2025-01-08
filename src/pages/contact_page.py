import dash_bootstrap_components as dbc
from dash import Dash, html


def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            dbc.Col(
                [
                    html.H1("Contact"),
                    html.P("You can contact us at:"),
                    html.P("Email", href="mailto:oliver.guggenbuehl@gmail.com"),
                ],
                width={
                    "size": 6,
                    "offset": 3,
                },
            ),
        ]
    )
