import dash_leaflet as dl
from dash import html

from components import constants, current_filters, ids, infobox
from components.widgets import action_button, color_mode, map_mode, type, year


def create_map_layer() -> dl.Map:
    """Create the main map layer with CartoDB Positron raster tiles and GeoJSON."""
    url = "https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"
    attribution = '&copy; <a href="https://carto.com/">CartoDB</a> contributors'

    return dl.Map(
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
    )


def create_top_controls() -> html.Div:
    """Create the top control panel with info box, mode controls, and action buttons."""
    return html.Div(
        children=[
            # Left column: Info box
            html.Div(
                children=[
                    infobox.render(top="0px", bottom=None, right=None, left="100px")
                ],
                className="left-column",
            ),
            # Center column: Map mode and type controls
            html.Div(
                children=[
                    map_mode.render(top="0px", bottom=None, right=None, left=None),
                    type.render(ids.TYPE_DROPDOWN),
                ],
                className="center-column",
            ),
            # Right column: Action buttons
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
                className="right-column",
            ),
        ],
        className="control-panel top-control-panel",
    )


def create_legend_controls() -> html.Div:
    """Create the left side of bottom controls with color legend and color mode selector."""
    return html.Div(
        [
            html.Div(
                id=ids.COLOR_LEGEND_CONTAINER,
                className="map-widget legend-container",
            ),
            html.Div(
                color_mode.render(),
                id="color-mode-container",
                className="map-widget color-mode-container",
            ),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "flex-end",
        },
    )


def create_bottom_controls() -> html.Div:
    """Create the bottom control panel with legend, year slider, and filters display."""
    return html.Div(
        children=[
            # Left: Legend and color mode
            create_legend_controls(),
            # Center: Year slider
            html.Div(
                year.render(id=ids.YEAR_SLIDER),
                id="year-slider-container",
                className="map-widget year-slider-container",
            ),
            # Right: Current filters display
            html.Div(
                current_filters.render(),
                id="current-filters-container",
                className="map-widget filters-container",
            ),
        ],
        className="control-panel bottom-control-panel",
    )


def render() -> html.Div:
    return html.Div(
        children=[
            create_top_controls(),
            create_map_layer(),
            create_bottom_controls(),
        ],
        className="map-container",
    )
