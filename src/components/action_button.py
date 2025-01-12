import dash_bootstrap_components as dbc
from dash import html


def render(
    name: str,
    id: str,
    **position_styles,
) -> html.Div:
    """Render an action button with flexible positioning.

    Args:
        name (str): The label displayed on the button.
        id (str): The unique identifier for the button.
        **position_styles: Optional CSS positioning styles (top, bottom, left, right).

    Returns:
        html.Div: A Dash HTML Div containing a styled button.
    """
    return html.Div(
        dbc.Button(
            name,
            id=id,
            n_clicks=0,
        ),
        style={
            **position_styles,
            "position": "absolute",
            "zIndex": "1000",
        },
    )
