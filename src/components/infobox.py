from dash import html

from components import ids


def render(top: str, bottom: str, right: str, left: str):
    # Return an empty Div that will be filled by the callback
    return html.Div(
        id=ids.INFOBOX,
        className=ids.INFOBOX,
        style={
            "position": "absolute",
            "top": top,
            "bottom": bottom,
            "right": right,
            "left": left,
        },
    )
