import dash_bootstrap_components as dbc
from dash import html

from components import (
    datatable,
    ids,
    map,
    sidebar,
)


def render() -> html.Div:
    return html.Div(
        id="map-page",
        children=[
            dbc.Col(
                [
                    _create_sidebar(),
                    _create_map_section(),
                    html.Br(),
                    _create_datatable_section(),
                ],
                width={"size": 12, "offset": 0},
            ),
        ],
    )


def _create_sidebar() -> html.Div:
    """
    Create the sidebar with filter controls.

    Returns:
        html.Div: The sidebar component
    """
    return sidebar.render()


def _create_map_section() -> dbc.Row:
    """
    Create the map visualization section.

    Returns:
        dbc.Row: A Bootstrap row containing the map component
    """
    return dbc.Row(
        dbc.Col(
            html.Div(
                className="map-container",
                children=[
                    dbc.Card(
                        map.render(),
                        body=True,
                        className="map-card",
                    )
                ],
            ),
            width=12,
        )
    )


def _create_datatable_section() -> dbc.Row:
    """
    Create the data table section for displaying tabular data.

    Returns:
        dbc.Row: A Bootstrap row containing the data table component
    """
    return dbc.Row(
        dbc.Col(
            html.Div(
                className="datatable-container",
                children=[
                    dbc.Card(
                        datatable.render(id=ids.DATATABLE),
                        body=True,
                        id="datatable-card",
                    )
                ],
            ),
            width=12,
        )
    )
