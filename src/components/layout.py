import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

from components import (
    constants,
    ids,
    navbar,
)


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-container",
        children=[
            dcc.Location(id=ids.URL, refresh=False),
            navbar.render(app),
            dcc.Store(id=ids.STORED_DATA),  # storage for queried dataset
            dcc.Store(id=ids.MODE_DATA),  # storage for mode data
            dcc.Store(id=ids.STORED_GEOJSON),  # storage for geojson
            dcc.Store(
                id=ids.DOWNLOAD_QUERIED_DATA
            ),  # storage for data to be downloaded
            dcc.Download(id=ids.DOWNLOAD_TRIGGER),
            dcc.Store(  # storage for the initial map state
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
