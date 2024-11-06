from components import ids
from dash import html


def render():
    # Return an empty Div that will be filled by the callback
    return html.Div(
        id=ids.INFOBOX_ADAPTATION,
        className=ids.INFOBOX,
        style={
            # "position": "absolute"
            "zIndex": "1000",
        },
    )
