import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

from climatefinancebert_ui.components import constants, datatable, ids, map, navbar, sidebar

initial_center = [51.4934, 0.0098]
initial_zoom = 2


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-container",
        children=[
            navbar.render(app),
            dcc.Store(id=ids.STORED_DATA),  # The store to keep the selected dataset
            dcc.Store(
                id=ids.INITIAL_STATE,
                data={
                    "center": initial_center,
                    "zoom": initial_zoom,
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
