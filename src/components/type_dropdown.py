from components import ids
from dash import Dash, dcc, html


def render(app: Dash) -> html.Div:
    types = ["donors", "recipients"]

    return html.Div(
        children=[
            html.H6("Type"),
            dcc.Dropdown(
                id=ids.TYPE_DROPDOWN,
                options=[{"label": type.title(), "value": type} for type in types],
                value="donors",
                multi=False,
            ),
        ]
    )
