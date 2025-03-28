from dash import dcc, html

from components.constants import FLOW_TYPES


def render(id: str, style: dict = None) -> html.Div:
    return html.Div(
        children=[
            html.H6("Flow Type"),
            dcc.Dropdown(
                id=id,
                options=FLOW_TYPES,
                value=["ODA Grants"],
                multi=True,
                style=style,
            ),
        ]
    )
