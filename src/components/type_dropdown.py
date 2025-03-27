from dash import dcc, html

from components import ids


def render() -> html.Div:
    types = ["donors", "recipients"]

    return html.Div(
        children=[
            html.H6("Donors or Recipients?"),
            dcc.Dropdown(
                id=ids.TYPE_DROPDOWN,
                options=[{"label": type.title(), "value": type} for type in types],
                value="donors",
                multi=False,
            ),
        ]
    )
