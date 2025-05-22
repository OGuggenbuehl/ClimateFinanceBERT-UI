import dash_bootstrap_components as dbc
from dash import html


def render(
    label: str,
    id: str,
    color: str = "primary",
    class_name: str = None,
    **position_styles,
) -> html.Div:
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
