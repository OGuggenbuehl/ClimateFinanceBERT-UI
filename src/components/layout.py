import dash_bootstrap_components as dbc
from components import (
    constants,
    datatable,
    ids,
    map,
    navbar,
    sidebar,
)
from dash import Dash, dcc, html


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-container",
        children=[
            navbar.render(app),
            dcc.Store(id=ids.STORED_DATA),  # The store to keep the selected dataset
            dcc.Store(id=ids.STORED_GEOJSON),  # The store to keep the geojson data
            dcc.Store(  # The store to keep the initial state of the map
                id=ids.INITIAL_STATE,
                data={
                    "center": constants.INITIAL_CENTER,
                    "zoom": constants.INITIAL_ZOOM,
                },
            ),
            dbc.Container(
                fluid=True,  # Set the container to be fluid
                children=[
                    dbc.Col(
                        [
                            sidebar.render(app),
                            dbc.Row(
                                dbc.Col(
                                    html.Div(
                                        className="map-container",
                                        children=[
                                            dbc.Card(
                                                map.render(app),
                                                body=True,
                                                className="map-card",
                                            )
                                        ],
                                    ),
                                    width=12,
                                )
                            ),
                            html.Br(),
                            dbc.Row(
                                dbc.Col(
                                    html.Div(
                                        className="datatable-container",
                                        children=[
                                            dbc.Card(
                                                datatable.render(),
                                                body=True,
                                            )
                                        ],
                                    ),
                                    width=12,
                                )
                            ),
                        ],
                        width={
                            "size": 12,
                            "offset": 0,
                        },
                    ),
                ],
            ),
        ],
    )
