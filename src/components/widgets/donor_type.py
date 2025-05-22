from typing import Optional

from dash import dcc, html

# Mapping from internal values to display labels
DONOR_TYPE_MAP = {
    "bilateral": "Donor Country",
    "multilateral": "Multilateral Donor",
    "private": "Private Donor",
}


def render(id: str, style: Optional[dict] = None) -> html.Div:
    return html.Div(
        children=[
            _create_heading(),
            _create_dropdown(id, style),
        ]
    )


def _create_heading() -> html.H6:
    """
    Create the heading for the donor type dropdown.

    Returns:
        html.H6: A heading element with the title text
    """
    return html.H6("Donor Type")


def _create_dropdown(id: str, style: Optional[dict] = None) -> dcc.Dropdown:
    """
    Create the dropdown for selecting donor types.

    Args:
        id: The ID to be assigned to the dropdown component
        style: Optional CSS styles to be applied to the dropdown

    Returns:
        dcc.Dropdown: A Dash Dropdown component for donor type selection
    """
    return dcc.Dropdown(
        id=id,
        options=_get_donor_type_options(),
        value=DONOR_TYPE_MAP["bilateral"],
        multi=True,
        style=style,
    )


def _get_donor_type_options() -> list[dict[str, str]]:
    """
    Get the list of donor type options with formatted labels.

    Returns:
        list[dict[str, str]]: A list of option dictionaries for the dropdown
    """
    return [
        {"label": donor_type.title(), "value": DONOR_TYPE_MAP[donor_type]}
        for donor_type in DONOR_TYPE_MAP
    ]
