import dash_leaflet as dl
import pandas as pd
from dash import Input, Output, State, dash
from dash_extensions.javascript import arrow_function

from climatefinancebert_ui.components import constants, ids, infobox_country, reset_button
from climatefinancebert_ui.components.utils import merge_data, prepare_data_for_merge


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
    )
    def update_map(
        stored_geojson,
    ):
        return [
            dl.TileLayer(),
            dl.GeoJSON(
                id=ids.COUNTRIES_LAYER,
                data=stored_geojson,
                hoverStyle=arrow_function(dict(weight=4, color="#666", dashArray="")),
                zoomToBoundsOnClick=True,
                interactive=True,
            ),
            infobox_country.render(top="20px", bottom=None, right=None, left="100px"),
            reset_button.render(top="20px", bottom=None, right="100px", left=None),
        ]
