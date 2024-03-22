import dash_bootstrap_components as dbc
from dash import html

import climatefinancebert_ui.components.ids as ids


def render(top: str, bottom: str, right: str, left: str):
    return html.Div(
        dbc.Button(
            "Reset Map",
            id=ids.RESET_MAP,
            n_clicks=0,
        ),
        style={
            "position": "absolute",
            "top": top,
            "bottom": bottom,
            "right": right,
            "left": left,
            "zIndex": "1000",
        },
    )
