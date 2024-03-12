import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

from climatefinancebert_ui.components import datatable, ids, map, navbar, sidebar


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-container",
        children=[
            navbar.render(app),
            dcc.Store(id=ids.STORED_DATA),  # The store to keep the selected dataset
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
                                                datatable.render(app),
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
