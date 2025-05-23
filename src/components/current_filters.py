from dash import html

from components import ids


def render(class_name: str = "map-widget", **position_styles) -> html.Div:
    return html.Div(
        id=ids.CURRENT_FILTERS,
        className=class_name,
        style={
            "padding": "10px",  # Add some padding
            **position_styles,
        },
    )
