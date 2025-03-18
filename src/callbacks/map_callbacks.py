import copy

import dash_leaflet as dl
import pandas as pd
from dash import Input, Output, State, dash
from dash_extensions.javascript import arrow_function

from components import constants, ids
from components.slider_player import PlaybackSliderAIO
from functions.data_operations import create_mode_data, merge_data
from functions.map_styler import style_map


def register(app):
    @app.callback(
        Output(ids.MAP, "center"),
        Output(ids.MAP, "zoom"),
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
            Input(ids.STORED_DATA, "data"),
            Input(ids.CATEGORIES_DROPDOWN, "value"),
            Input(ids.CATEGORIES_SUB_DROPDOWN, "value"),
            Input(ids.MAP_MODE, "value"),
            Input(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER), "value"),
        ],
        prevent_initial_call=True,
    )
    # TODO: when to update and does aggregation really need to be done after storing?
    def update_stored_geojson(
        stored_data,
        selected_categories,
        selected_subcategories,
        map_mode,
        selected_year,
    ):
        # retrieve stored dataframe and parse geojson
        df_stored = pd.DataFrame(stored_data)

        # prepare data for merging
        df_mode = create_mode_data(
            df_stored,
            map_mode,
            selected_categories,
            selected_subcategories,
        )

        # Create a deep copy of the base geojson to ensure it is not altered
        geojson_copy = copy.deepcopy(constants.GEOJSON_BASE)

        return merge_data(geojson_copy, df_mode)

    @app.callback(
        Output(ids.MAP, "children"),
        Input(ids.STORED_GEOJSON, "data"),
        Input(ids.MAP_MODE, "value"),
    )
    def update_map(
        stored_geojson,
        map_mode_value,
    ):
        if map_mode_value == "base":
            return [
                dl.TileLayer(),
                # render dummy map to be replaced by the callback
                dl.GeoJSON(
                    url=constants.GEOJSON_URL,
                    id=ids.COUNTRIES_LAYER,
                    style=style_map(map_mode_value),
                    hoverStyle=arrow_function(
                        dict(weight=4, color="#666", dashArray="")
                    ),
                ),
            ]
        else:
            classes, colorscale, style, style_handle = style_map(map_mode_value)
            return [
                dl.TileLayer(),
                dl.GeoJSON(
                    id=ids.COUNTRIES_LAYER,
                    data=stored_geojson,
                    style=style_handle,  # how to style each polygon
                    # TODO: comment out due to buggy hover behavior
                    hoverStyle=arrow_function(
                        dict(weight=4, color="#666", dashArray="")
                    ),  # style applied on hover
                    hideout=dict(
                        colorscale=colorscale,
                        classes=classes,
                        style=style,
                        polyColoring="value",
                    ),
                    zoomToBoundsOnClick=True,
                    interactive=True,
                ),
            ]
