import copy

import dash_leaflet as dl
import pandas as pd
from components import constants, ids
from dash import Input, Output, State, dash
from dash_extensions.javascript import arrow_function, assign
from functions.data_operations import create_mode_data, merge_data
from functions.map_styler import style_map

# TODO: move to constants
classes = [0, 10, 20, 50, 100, 200, 500, 1000]
colorscale = [
    "#A9A9A9",
    "#FED976",
    "#FEB24C",
    "#FD8D3C",
    "#FC4E2A",
    "#E31A1C",
    "#BD0026",
    "#800026",
]
style = dict(weight=2, opacity=1, color="white", dashArray="3", fillOpacity=0.7)

# Geojson rendering logic, must be JavaScript as it is executed in clientside.
style_handle = assign("""function(feature, context){
    const {classes, colorscale, style, polyColoring} = context.hideout;  // get props from hideout
    const value = feature.properties[polyColoring];  // get value the determines the color
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}""")


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
        prevent_initial_call=True,
    )
    # TODO: when to update and does aggregation really need to be done after storing?
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
