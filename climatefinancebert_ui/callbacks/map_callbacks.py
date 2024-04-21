import dash_leaflet as dl
import pandas as pd
from dash import Input, Output, State, dash
from dash_extensions.javascript import arrow_function, assign

from climatefinancebert_ui.components import constants, ids, infobox_country, map_mode, reset_button
from climatefinancebert_ui.components.utils import merge_data, prepare_data_for_merge

classes = [0, 10, 20, 50, 100, 200, 500, 1000]
colorscale = [
    "#eeeeee",
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
        ],
    )
    def update_stored_geojson(
        stored_data,
        selected_categories,
    ):
        # retrieve stored dataframe and parse geojson
        df_stored = pd.DataFrame(stored_data)

        # prepare data for merging
        df_prepared = prepare_data_for_merge(
            df_stored,
            selected_categories=selected_categories,
        )

        return merge_data(constants.GEOJSON_BASE, df_prepared)

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
                    style={"fillColor": "dodgerblue", "color": "dodgerblue"},
                ),
                infobox_country.render(top="20px", bottom=None, right=None, left="100px"),
                reset_button.render(top="20px", bottom=None, right="100px", left=None),
            ]
        elif map_mode_value == "total":
            return [
                dl.TileLayer(),
                dl.GeoJSON(
                    id=ids.COUNTRIES_LAYER,
                    data=stored_geojson,
                    style=style_handle,  # how to style each polygon
                    hoverStyle=arrow_function(
                        dict(weight=5, color="#666", dashArray="")
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
                infobox_country.render(top="20px", bottom=None, right=None, left="100px"),
                reset_button.render(top="20px", bottom=None, right="100px", left=None),
            ]
