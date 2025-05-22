from dash import html

from components import ids


def render(
    top: str = None, bottom: str = None, right: str = None, left: str = None
) -> html.Div:
    # Set position style only for non-None values to avoid "None" as string in style
    position_style = {}
    if top is not None:
        position_style["top"] = top
    if bottom is not None:
        position_style["bottom"] = bottom
    if right is not None:
        position_style["right"] = right
    if left is not None:
        position_style["left"] = left

    return html.Div(
        id=ids.INFOBOX,
        className="infobox map-widget",
        style={
            "position": "absolute",
            **position_style,
        },
    )
