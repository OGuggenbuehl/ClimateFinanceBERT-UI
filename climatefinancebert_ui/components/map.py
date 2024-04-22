import dash_leaflet as dl
from dash import Dash, html

from climatefinancebert_ui.components import (
    constants,
    ids,
    infobox_adaptation,
    infobox_climatefinance,
    infobox_country,
    infobox_environment,
    infobox_mitigation,
    map_mode,
    reset_button,
)


def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            html.Div(
                children=[
                    infobox_country.render(top="0px", bottom=None, right=None, left="100px"),
                    map_mode.render(top="0px", bottom=None, right="500px", left=None),
                    reset_button.render(top="0px", bottom=None, right="100px", left=None),
                ],
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "justifyContent": "space-around",
                    "alignItems": "center",
                    "position": "absolute",
                    "top": "20px",
                    "left": 0,
                    "right": 0,
                    "padding": "0 20px",
                },
            ),
            dl.Map(
                children=[
                    dl.TileLayer(),
                    # render dummy map to be replaced by the callback
                    dl.GeoJSON(
                        url=constants.GEOJSON_URL,
                        id=ids.COUNTRIES_LAYER,
                        style={"fillColor": "dodgerblue", "color": "dodgerblue"},
                        # hoverStyle=arrow_function(dict(weight=4, color="#666", dashArray="")),
                        zoomToBoundsOnClick=True,
                        # zoomToBounds=True,
                        interactive=True,
                    ),
                    infobox_country.render(top="20px", bottom=None, right=None, left="100px"),
                    reset_button.render(top="20px", bottom=None, right="100px", left=None),
                ],
                id=ids.MAP,
                center=constants.INITIAL_CENTER,
                zoom=constants.INITIAL_ZOOM,
                style={"height": "85vh"},
                maxZoom=5,
                minZoom=2,
                maxBounds=[[-90, -180], [90, 180]],
                maxBoundsViscosity=1.0,
                scrollWheelZoom=False,
            ),
            html.Div(
                children=[
                    # infobox_climatefinance.render(),
                    infobox_environment.render(),
                    infobox_adaptation.render(),
                    infobox_mitigation.render(),
                ],
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "justifyContent": "space-around",
                    "alignItems": "center",
                    "position": "absolute",
                    "bottom": "20px",
                    "left": 0,
                    "right": 0,
                    "padding": "0 20px",
                },
            ),
        ],
        style={"position": "relative"},
    )
