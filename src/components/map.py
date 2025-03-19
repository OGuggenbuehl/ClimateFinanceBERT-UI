import dash_leaflet as dl
from dash import Dash, html

from components import (
    action_button,
    constants,
    ids,
    infobox_adaptation,
    infobox_country,
    infobox_environment,
    infobox_mitigation,
    map_mode,
)


def render(app: Dash) -> html.Div:
    url = "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
    attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '
    return html.Div(
        children=[
            html.Div(
                children=[
                    infobox_country.render(
                        top="0px", bottom=None, right=None, left="100px"
                    ),
                    map_mode.render(top="0px", bottom=None, right="37.5%", left=None),
                    action_button.render(
                        name="Open Filters 🔍",
                        id=ids.OPEN_FILTERS,
                        top="0px",
                        right="100px",
                    ),
                    action_button.render(
                        name="Reset Map ↪️",
                        id=ids.RESET_MAP,
                        top="50px",
                        right="100px",
                    ),
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
                id=ids.MAP,
                children=[
                    dl.TileLayer(
                        url=url,
                        # maxZoom=5,
                        # minZoom=2,
                        attribution=attribution,
                    ),
                    # render dummy map to be replaced by the callback
                    dl.GeoJSON(
                        url=constants.GEOJSON_URL,
                        id=ids.COUNTRIES_LAYER,
                        style={"fillColor": "dodgerblue", "color": "dodgerblue"},
                    ),
                ],
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
