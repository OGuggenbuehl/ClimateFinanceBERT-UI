from typing import Optional

from dash import dcc, html

from components.constants import CATEGORIES_DF


def render(id: str, style: Optional[dict] = None) -> html.Div:
    return html.Div(
        children=[
            _create_heading(),
            _create_dropdown(id, style),
        ]
    )


def _create_heading() -> html.H6:
    """
    Create the heading for the categories dropdown.

    Returns:
        html.H6: A heading element with the title text
    """
    return html.H6("Categories")


def _create_dropdown(id: str, style: Optional[dict] = None) -> dcc.Dropdown:
    """
    Create the dropdown for selecting categories.

    Args:
        id: The ID to be assigned to the dropdown component
        style: Optional CSS styles to be applied to the dropdown

    Returns:
        dcc.Dropdown: A Dash Dropdown component for category selection
    """
    return dcc.Dropdown(
        id=id,
        options=_get_category_options(),
        value=["Mitigation"],  # CATEGORIES_DF["climate_class"].unique(),
        multi=True,
        style=style,
    )


def _get_category_options() -> list[str]:
    """
    Get the list of available category options.

    Returns:
        List[str]: A list of unique category values
    """
    return CATEGORIES_DF["climate_class"].unique()
