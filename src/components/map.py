import dash_leaflet as dl
from dash import html

from components import (
    constants,
    ids,
    infobox,
)
from components.widgets import action_button, map_mode, type, year


def render() -> html.Div:
    url = "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
    attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '

    return html.Div(
        children=[
            html.Div(
                children=[
                    # Infobox on the left
                    html.Div(
                        children=[
                            infobox.render(
                                top="0px", bottom=None, right=None, left="100px"
                            )
                        ],
                        style={
                            "gridColumn": "1",  # Place infobox in the first column
                            "zIndex": 10,  # Ensure infobox is above the map
                        },
                    ),
                    # map-mode selector in the center
                    html.Div(
                        children=[
                            map_mode.render(
                                top="0px", bottom=None, right=None, left=None
                            ),
                            type.render(ids.TYPE_DROPDOWN),
                        ],
                        style={
                            "gridColumn": "2",  # Place map-mode selector in the second (middle) column
                            "zIndex": 10,  # Ensure map-mode is above the map
                            "textAlign": "center",  # Center the map-mode
                            "maxWidth": "600px",  # Limit the width of the map-mode selector
                            "margin": "0 auto",  # Horizontally center the map-mode selector
                        },
                    ),
                    # Action buttons on the right
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
                        style={
                            "gridColumn": "3",  # Place action buttons in the third column
                            "zIndex": 10,  # Ensure buttons are above the map
                            "textAlign": "right",  # Align buttons to the right
                        },
                    ),
                ],
                style={
                    "display": "grid",  # Use CSS Grid for layout
                    "gridTemplateColumns": "auto 1fr auto",  # Create 3 columns: left, center, right
                    "alignItems": "center",  # Vertically center all items
                    "position": "absolute",
                    "top": "20px",
                    "left": 0,
                    "right": 0,
                    "padding": "0 20px",
                    "zIndex": 10,  # Ensure controls are above the map
                },
            ),
            dl.Map(
                id=ids.MAP,
                children=[
                    dl.TileLayer(
                        url=url,
                        attribution=attribution,
                    ),
                    dl.GeoJSON(
                        url=constants.GEOJSON_URL,
                        id=ids.COUNTRIES_LAYER,
                        style={
                            "color": "dodgerblue",
                            "opacity": 0,  # hide layer for now
                            "fillColor": "dodgerblue",
                            "fillOpacity": 0,  # hide layer for now
                        },
                    ),
                ],
                center=constants.INITIAL_CENTER,
                zoom=constants.INITIAL_ZOOM,
                style={"height": "85vh", "zIndex": 1},  # Lower z-index for the map
                maxZoom=5,
                minZoom=2,
                maxBounds=[[-90, -180], [90, 180]],
                maxBoundsViscosity=1.0,
                scrollWheelZoom=False,
            ),
            html.Div(
                children=[year.render(id=ids.YEAR_SLIDER)],
                className=ids.INFOBOX,
                style={
                    "position": "absolute",
                    "bottom": "-40px",
                    "left": "50%",  # Horizontally center the div
                    "transform": "translate(-50%, -50%)",  # Offset the div by half of its width and height
                    "zIndex": 10,
                    "width": "80%",
                    "maxWidth": "600px",
                    "padding": "10px",
                    "border": "1px solid #ccc",
                    "borderRadius": "8px",
                    "backgroundColor": "rgba(255, 255, 255, 0.7)",
                },
            ),
        ],
        style={"position": "relative"},
    )
