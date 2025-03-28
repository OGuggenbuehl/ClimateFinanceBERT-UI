import logging
import time

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, dash_table, html
from dash.exceptions import PreventUpdate

from components import ids
from components.constants import CATEGORIES_DF, DUCKDB_PATH
from components.slider_player import PlaybackSliderAIO
from functions.data_operations import create_mode_data, reshape_by_type
from functions.query_duckdb import construct_query, query_duckdb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register(app):
    @app.callback(
        Output(ids.STORED_DATA, "data"),
        [
            Input(ids.TYPE_DROPDOWN, "value"),
            Input(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER), "value"),
            Input(ids.DONORTYPE_DROPDOWN, "value"),
            Input(ids.CATEGORIES_DROPDOWN, "value"),
            Input(ids.CATEGORIES_SUB_DROPDOWN, "value"),
            Input(ids.FLOW_TYPE_DROPDOWN, "value"),
        ],
        prevent_initial_call=True,
    )
    def update_stored_data(
        selected_type,
        selected_year,
        selected_donor_types,
        selected_categories,
        selected_subcategories,
        selected_flow_types,
    ):
        """Reads, subsets and stores data based on the set UI inputs.

        Args:
            selected_type (str): Either 'donors' or 'recipients'
            selected_year (int): An integer representing the selected year.

        Returns:
            list(dict): The stored data as a list of dictionaries.
        """
        start = time.time()
        query = construct_query(
            year_type="single_year",
            selected_year=selected_year,
            selected_categories=selected_categories,
            selected_subcategories=selected_subcategories,
            selected_donor_types=selected_donor_types,
            selected_flow_types=selected_flow_types,
        )

        df_queried = query_duckdb(
            duckdb_db=DUCKDB_PATH,
            query=query,
        )
        df_reshaped = reshape_by_type(df_queried, selected_type)

        end = time.time()
        logger.info(
            f"Execution time for updating stored data: {end - start:.2f} seconds."
        )
        return df_reshaped.to_dict("records")  # list of dicts as storage format

    @app.callback(
        Output(ids.MODE_DATA, "data"),
        [
            Input(ids.MAP_MODE, "value"),
            Input(ids.STORED_DATA, "data"),
            Input(ids.CATEGORIES_DROPDOWN, "value"),
            Input(ids.CATEGORIES_SUB_DROPDOWN, "value"),
        ],
        prevent_initial_call=True,
    )
    def update_mode_data(
        map_mode,
        stored_data,
        selected_categories,
        selected_subcategories,
    ):
        if map_mode != "base":
            df = pd.DataFrame(stored_data)
            df_mode = create_mode_data(
                df,
                map_mode,
                selected_categories,
                selected_subcategories,
            )
            return df_mode.to_dict("records")
        return []  # return empty list if map mode is set to 'base'

    @app.callback(
        Output(ids.CATEGORIES_SUB_DROPDOWN, "options"),
        Input(ids.CATEGORIES_DROPDOWN, "value"),
        prevent_initial_call=False,
    )
    def set_meta_options(selected_climate_class):
        # subset the available meta_categories based on the selected climate class
        filtered_df = CATEGORIES_DF[
            CATEGORIES_DF["climate_class"].isin(selected_climate_class)
        ]

        return [{"label": i, "value": i} for i in filtered_df["meta_category"].unique()]

    @app.callback(
        Output(ids.DATATABLE, "children"),
        [
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.MODE_DATA, "data"),
        ],
        prevent_initial_call=True,
    )
    def build_datatable(
        click_data=None,
        mode_data=None,
    ):
        """Build the datatable based on the input elements and the selected map element."""
        if not click_data:
            return html.H4("Click a country to render a datatable")
        else:
            # build the info header based on the clicked country
            country_name = click_data["properties"]["name"]
            header = [html.H4(f"Data for {country_name}:")]

            # subset the data based on the selected country
            country_code = click_data["id"]
            df_mode = pd.DataFrame(mode_data)

            # filter the data based on the selected country
            try:
                df_filtered = df_mode[df_mode["CountryCode"] == country_code]
            # this is needed to circumvent an error where filtering on a country
            # that has no data available for the selected categories and years
            # leads to a KeyError
            except KeyError:
                return header + [html.H4("No data available for this country.")]

            if len(df_filtered) == 0:
                return header + [
                    html.H4(
                        "No data available for this country for the selected filters."
                    )
                ]
            else:
                # render DataTable with the filtered data
                return header + [
                    dash_table.DataTable(
                        data=df_filtered.to_dict("records"),
                        columns=[{"name": i, "id": i} for i in df_filtered.columns],
                        page_size=15,
                        sort_action="native",
                        style_cell={
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "maxWidth": 0,
                        },
                    )
                ]

    @app.callback(
        Output(ids.FLOW_DATA_TABLE, "children"),
        [
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.STORED_DATA, "data"),
            Input(ids.FLOW_DATA_BTN, "n_clicks"),
            Input(ids.FLOW_DATA_MODAL, "is_open"),
        ],
    )
    def build_flow_data_table(
        click_data,
        stored_data,
        n_clicks,
        is_open,
    ):
        if n_clicks is None or not is_open:
            raise PreventUpdate

        start = time.time()
        # build the info header based on the clicked country
        country_name = click_data["properties"]["name"]
        header = [html.H4(f"Flow Data for {country_name}:")]

        # subset the data based on the selected country
        country_code = click_data["id"]
        df = pd.DataFrame(stored_data)

        # filter the data based on the selected country
        try:
            df_filtered = df[df["CountryCode"] == country_code]
        # this is needed to circumvent an error where filtering on a country
        # that has no data available for the selected categories and years
        # leads to a KeyError
        except KeyError:
            return [
                dbc.ModalHeader(dbc.ModalTitle(header)),
                dbc.ModalBody(html.H4("No data available for this country.")),
                dbc.ModalFooter(),
            ]

        if len(df_filtered) == 0:
            return [
                dbc.ModalHeader(dbc.ModalTitle(header)),
                dbc.ModalBody(
                    html.H4(
                        "No data available for this country for the selected filters."
                    )
                ),
                dbc.ModalFooter(),
            ]
        else:
            end = time.time()
            logger.info(
                f"Execution time for building flow data table: {end - start:.2f} seconds."
            )
            return [
                dbc.ModalHeader(dbc.ModalTitle(header)),
                dbc.ModalBody(
                    dash_table.DataTable(
                        data=df_filtered.to_dict("records"),
                        columns=[{"name": i, "id": i} for i in df_filtered.columns],
                        page_size=15,
                        sort_action="native",
                        style_cell={
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "maxWidth": 0,
                        },
                    )
                ),
                dbc.ModalFooter(),
            ]

    @app.callback(
        Output(ids.DATATABLE_CARD, "style"),
        Input(ids.MAP_MODE, "value"),
    )
    def toggle_table_visibility(map_mode):
        if map_mode == "base":
            return {"display": "none"}  # Hide the table
        return {"display": "block"}  # Show the table
