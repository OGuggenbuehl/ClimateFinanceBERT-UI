import dash_leaflet as dl
from dash import html

from components import (
    constants,
    ids,
    infobox,
)
from components.widgets import action_button, color_mode, map_mode, type, year


def render() -> html.Div:
    url = "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
    attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '

    return html.Div(
        children=[
            # Top control row
            html.Div(
                children=[
                    html.Div(
                        children=[
                            infobox.render(
                                top="0px", bottom=None, right=None, left="100px"
                            )
                        ],
                        style={"gridColumn": "1", "zIndex": 10},
                    ),
                    html.Div(
                        children=[
                            map_mode.render(
                                top="0px", bottom=None, right=None, left=None
                            ),
                            type.render(ids.TYPE_DROPDOWN),
                        ],
                        style={
                            "gridColumn": "2",
                            "zIndex": 10,
                            "textAlign": "center",
                            "maxWidth": "600px",
                            "margin": "0 auto",
                        },
                    ),
                    html.Div(
                        children=[
                            action_button.render(
                                "Open Filters 🔍",
                                id=ids.OPEN_FILTERS,
                                top="0px",
                                right="100px",
                                position="absolute",
                            ),
                            action_button.render(
                                "Reset Map ↪️",
                                id=ids.RESET_MAP,
                                top="50px",
                                right="100px",
                                position="absolute",
                            ),
                        ],
                        style={"gridColumn": "3", "zIndex": 10, "textAlign": "right"},
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "auto 1fr auto",
                    "alignItems": "center",
                    "position": "absolute",
                    "top": "20px",
                    "left": 0,
                    "right": 0,
                    "padding": "0 20px",
                    "zIndex": 10,
                },
            ),
            # Main map
            dl.Map(
                id=ids.MAP,
                children=[
                    dl.TileLayer(url=url, attribution=attribution),
                    dl.GeoJSON(
                        url=constants.GEOJSON_URL,
                        id=ids.COUNTRIES_LAYER,
                        style={
                            "color": "dodgerblue",
                            "opacity": 0,
                            "fillColor": "dodgerblue",
                            "fillOpacity": 0,
                        },
                    ),
                ],
                center=constants.INITIAL_CENTER,
                zoom=constants.INITIAL_ZOOM,
                style={"height": "85vh", "zIndex": 1},
                maxZoom=5,
                minZoom=2,
                maxBounds=[[-90, -180], [90, 180]],
                maxBoundsViscosity=1.0,
                scrollWheelZoom=False,
            ),
            # Bottom control row (legend, year slider, color mode)
            html.Div(
                children=[
                    html.Div(
                        id=ids.COLOR_LEGEND_CONTAINER,
                        style={
                            "width": "200px",  # fixed
                            "zIndex": "1000",
                            "padding": "6px 8px",
                        },
                    ),
                    html.Div(
                        year.render(id=ids.YEAR_SLIDER),
                        id="year-slider-container",
                        style={
                            "flex": "1",  # take remaining space
                            "maxWidth": "600px",
                            "margin": "0 auto",  # Center in the available space
                            "padding": "10px",
                            "border": "1px solid #ccc",
                            "borderRadius": "8px",
                            "backgroundColor": "rgba(255, 255, 255, 0.7)",
                        },
                    ),
                    html.Div(
                        color_mode.render(),
                        id="color-mode-container",
                        style={
                            "width": "200px",  # fixed
                            "zIndex": "1000",
                            "padding": "6px 8px",
                            "background": "rgba(255, 255, 255, 0.8)",
                            "boxShadow": "0 0 15px rgba(0, 0, 0, 0.2)",
                            "borderRadius": "5px",
                        },
                    ),
                ],
                style={
                    "position": "absolute",
                    "bottom": "10px",
                    "left": 0,
                    "right": 0,
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "padding": "0 40px",
                    "zIndex": 10,
                },
            ),
        ],
        style={"position": "relative"},
    )
