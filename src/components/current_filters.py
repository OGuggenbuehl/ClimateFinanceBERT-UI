from dash import html

from components import ids


def render(class_name: str = None, **position_styles) -> html.Div:
    # Return an empty Div that will be filled by the callback
    return html.Div(
        id=ids.CURRENT_FILTERS,
        className=class_name,
        style={
            **position_styles,
        },
    )
