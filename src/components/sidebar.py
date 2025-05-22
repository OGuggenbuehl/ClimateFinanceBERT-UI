import dash_bootstrap_components as dbc
from dash import html

from components import ids
from components.widgets import (
    categories,
    donor_type,
    flow_type,
    sub_categories,
)


def render() -> html.Div:
    return html.Div(
        [
            dbc.Offcanvas(
                [
                    _create_header(),
                    _create_filters_nav(),
                ],
                id="offcanvas",
                title=html.B("Filters"),
                is_open=False,
            ),
        ]
    )


def _create_header() -> html.P:
    """
    Create the header text for the sidebar.

    Returns:
        html.P: A paragraph element with instruction text
    """
    return html.P("Mix and match your selection to filter the data")


def _create_filters_nav() -> dbc.Nav:
    """
    Create the navigation component containing all filter widgets.

    Returns:
        dbc.Nav: A Bootstrap Nav component with all filter widgets
    """
    return dbc.Nav(
        [
            html.Hr(),
            donor_type.render(ids.DONORTYPE_DROPDOWN),
            html.Hr(),
            flow_type.render(ids.FLOW_TYPE_DROPDOWN),
            html.Hr(),
            categories.render(ids.CATEGORIES_DROPDOWN),
            html.Hr(),
            sub_categories.render(ids.CATEGORIES_SUB_DROPDOWN),
        ],
        vertical=True,
        pills=True,
    )
