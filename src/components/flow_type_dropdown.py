from dash import dcc, html

from components import ids
from components.constants import FLOW_TYPES


def render() -> html.Div:
    return html.Div(
        children=[
            html.H6("Flow Type"),
            dcc.Dropdown(
                id=ids.FLOW_TYPE_DROPDOWN,
                options=FLOW_TYPES,
                value=["ODA Grants"],
                multi=True,
            ),
        ]
    )
