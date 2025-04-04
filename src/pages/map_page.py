import dash_bootstrap_components as dbc
from dash import Dash, html

from components import (
    datatable,
    ids,
    map,
    sidebar,
)


def render(app: Dash) -> html.Div:
    return html.Div(
        id="map-page",
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
                                        map.render(),
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
                                        datatable.render(id=ids.DATATABLE),
                                        body=True,
                                        id="datatable-card",
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
    )
