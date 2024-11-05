from dash import Dash, dcc, html

from climatefinancebert_ui.components import ids


def render(app: Dash) -> html.Div:
    types = ["donors", "recipients"]

    return html.Div(
        children=[
            html.H6("Type"),
            dcc.Dropdown(
                id=ids.TYPE_DROPDOWN,
                options=[{"label": type.title(), "value": type} for type in types],
                value="recipients",
                multi=False,
            ),
        ]
    )
