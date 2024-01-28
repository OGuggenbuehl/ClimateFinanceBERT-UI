import dash_leaflet as dl
from dash import Dash, html
from dash_extensions.javascript import arrow_function

from climatefinancebert_ui.components import ids

url = (
    "https://raw.githubusercontent.com/"
    "johan/world.geo.json/master/countries.geo.json"
)


def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            dl.Map(
                [
                    dl.TileLayer(),
                    dl.GeoJSON(
                        url=url,
                        # zoomToBounds=True,
                        id=ids.COUNTRIES_LAYER,
                        hoverStyle=arrow_function(
                            dict(weight=4, color="#666", dashArray="")
                        ),
                        zoomToBoundsOnClick=False,
                        interactive=True
                        # hideout=dict(selected=[]),
                    ),
                ],
                id=ids.MAP,
                center=[51.4934, 0.0098],
                zoom=2,
                style={"height": "50vh"},
                maxZoom=5,
                minZoom=2,
            )
        ],
    )
