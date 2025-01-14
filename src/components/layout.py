import dash_bootstrap_components as dbc
from components import (
    constants,
    ids,
    navbar,
)
from dash import Dash, dcc, html


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-container",
        children=[
            dcc.Location(id=ids.URL, refresh=False),
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
                id=ids.PAGE_CONTENT,
                fluid=True,
            ),
        ],
    )
