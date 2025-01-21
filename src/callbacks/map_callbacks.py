import copy

import dash_leaflet as dl
import pandas as pd
from components import constants, ids
from dash import Input, Output, State, dash
from dash_extensions.javascript import arrow_function
from functions.data_operations import merge_data, prepare_data_for_merge
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
            Input(ids.YEAR_SLIDER, "value"),
            Input(ids.MAP_MODE, "value"),
        ],
    )
    def update_stored_geojson(
        stored_data,
        selected_categories,
        selected_subcategories,
        selected_years,
        map_mode,
    ):
        # retrieve stored dataframe and parse geojson
        df_stored = pd.DataFrame(stored_data)
        # prepare data for merging
        df_prepared = prepare_data_for_merge(
            df_stored,
            selected_categories=selected_categories,
            selected_subcategories=selected_subcategories,
            year_range=selected_years,
            map_mode=map_mode,
        )

        # Create a deep copy of the base geojson to ensure it is not altered
        geojson_copy = copy.deepcopy(constants.GEOJSON_BASE)

        return merge_data(geojson_copy, df_prepared)

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
