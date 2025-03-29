import dash_bootstrap_components as dbc
from dash import html


def render(
    label: str,
    id: str,
    color: str = "primary",
    class_name: str = None,
    **position_styles,
) -> html.Div:
    """Render an action button that spans the whole column with flexible positioning.

    Args:
        label (str): The label displayed on the button.
        id (str): The unique identifier for the button.
        **position_styles: Optional CSS positioning styles (top, bottom, left, right).

    Returns:
        html.Div: A Dash HTML Div containing a styled button.
    """
    return html.Div(
        dbc.Button(
            label,
            id=id,
            color=color,
            className=class_name,  # Makes the button span the full width of the column
            n_clicks=0,
        ),
        style={
            **position_styles,
        },
    )
