from typing import Optional

from dash import dcc, html

from components.constants import FLOW_TYPES


def render(id: str, style: Optional[dict] = None) -> html.Div:
    return html.Div(
        children=[
            _create_heading(),
            _create_dropdown(id, style),
        ]
    )


def _create_heading() -> html.H6:
    """
    Create the heading for the flow type dropdown.

    Returns:
        html.H6: A heading element with the title text
    """
    return html.H6("Flow Type")


def _create_dropdown(id: str, style: Optional[dict] = None) -> dcc.Dropdown:
    """
    Create the dropdown for selecting flow types.

    Args:
        id: The ID to be assigned to the dropdown component
        style: Optional CSS styles to be applied to the dropdown

    Returns:
        dcc.Dropdown: A Dash Dropdown component for flow type selection
    """
    return dcc.Dropdown(
        id=id,
        options=FLOW_TYPES,
        value=["ODA Grants"],
        multi=True,
        style=style,
    )
