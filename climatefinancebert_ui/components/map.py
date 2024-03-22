import dash_leaflet as dl
from dash import Dash, html
from dash_extensions.javascript import arrow_function

from climatefinancebert_ui.components import (
    ids,
    infobox_adaptation,
    infobox_climatefinance,
    infobox_country,
    infobox_environment,
    infobox_mitigation,
    reset_button,
)

url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"


def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            dl.Map(
                children=[
                    dl.TileLayer(),
                    dl.GeoJSON(
                        url=url,
                        id=ids.COUNTRIES_LAYER,
                        hoverStyle=arrow_function(dict(weight=4, color="#666", dashArray="")),
                        zoomToBoundsOnClick=True,
                        # zoomToBounds=True,
                        interactive=True,
                    ),
                    infobox_country.render(top="20px", bottom=None, right=None, left="100px"),
                    reset_button.render(top="20px", bottom=None, right="100px", left=None),
                ],
                id=ids.MAP,
                center=[51.4934, 0.0098],
                zoom=2,
                style={"height": "85vh"},
                maxZoom=5,
                minZoom=2,
                maxBounds=[[-90, -180], [90, 180]],
                maxBoundsViscosity=1.0,
                scrollWheelZoom=False,
            ),
            html.Div(
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
                children=[
                    infobox_climatefinance.render(),
                    infobox_environment.render(),
                    infobox_adaptation.render(),
                    infobox_mitigation.render(),
                ],
            ),
        ],
        style={"position": "relative"},
    )
