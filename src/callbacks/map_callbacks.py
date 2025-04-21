import copy

import dash_leaflet as dl
import pandas as pd
from dash import Input, Output, State, dash
from dash_extensions.javascript import arrow_function

from components import color_legend, constants, ids
from utils.data_operations import merge_data
from utils.map_styler import style_map


def register(app):
    @app.callback(
        [
            Output(ids.MAP, "center"),
            Output(ids.MAP, "zoom"),
        ],
        Input(ids.RESET_MAP, "n_clicks"),
        State(ids.INITIAL_STATE, "data"),
    )
    def reset_map(n_clicks, initial_state):
        if n_clicks > 0:
            return initial_state["center"], initial_state["zoom"]
        else:
            return dash.no_update, dash.no_update

    @app.callback(
        Output(ids.STORED_GEOJSON, "data"),
        [
            Input(ids.MODE_DATA, "data"),
            Input(ids.MAP_MODE, "value"),
        ],
        prevent_initial_call=True,
    )
    def update_stored_geojson(
        mode_data,
        map_mode,
    ):
        df_mode = pd.DataFrame(mode_data)
        geojson_copy = copy.deepcopy(constants.GEOJSON_BASE)
        return merge_data(df_mode, geojson_copy, map_mode)

    @app.callback(
        Output(ids.MAP, "children"),
        [
            Input(ids.STORED_GEOJSON, "data"),
            Input(ids.MAP_MODE, "value"),
            Input(ids.COLOR_MODE, "value"),
        ],
        prevent_initial_call=True,
    )
    def update_map(
        stored_geojson,
        map_mode_value,
        color_mode,
    ):
        url = (
            "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
        )
        attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '

        style_info = style_map(map_mode_value, color_mode, stored_geojson)

        if map_mode_value == "base":
            return [
                dl.TileLayer(url=url, attribution=attribution),
                dl.GeoJSON(
                    url=constants.GEOJSON_URL,
                    id=ids.COUNTRIES_LAYER,
                    style=style_info["style"],
                    hoverStyle=arrow_function(
                        dict(weight=4, color="#666", dashArray="")
                    ),
                ),
            ]
        else:
            # Create the base hideout dictionary
            hideout_dict = dict(
                polyColoring="value",
                style=style_info["style"],
                colorscale=style_info["colorscale"],
                min=style_info["min"],
                max=style_info["max"],
            )

            # Add quartile data if needed
            if color_mode == "quartile":
                hideout_dict.update(
                    {
                        "quartile_breaks": style_info["quartile_breaks"],
                        "quartile_colors": style_info["quartile_colors"],
                    }
                )

            return [
                dl.TileLayer(url=url, attribution=attribution),
                dl.GeoJSON(
                    id=ids.COUNTRIES_LAYER,
                    data=stored_geojson,
                    style=style_info["style_handle"],
                    hoverStyle=arrow_function(
                        dict(weight=4, color="#666", dashArray="")
                    ),
                    hideout=hideout_dict,
                    zoomToBoundsOnClick=True,
                    interactive=True,
                ),
            ]

    @app.callback(
        Output(ids.COLOR_LEGEND_CONTAINER, "children"),
        [
            Input(ids.STORED_GEOJSON, "data"),
            Input(ids.MAP_MODE, "value"),
            Input(ids.COLOR_MODE, "value"),
        ],
        prevent_initial_call=True,
    )
    def update_color_legend(stored_geojson, map_mode_value, color_mode):
        """Update the color legend based on current map data and settings."""
        if map_mode_value == "base":
            return []

        style_info = style_map(map_mode_value, color_mode, stored_geojson)
        legend = color_legend.render(map_mode_value, color_mode, style_info)

        return [legend] if legend else []
