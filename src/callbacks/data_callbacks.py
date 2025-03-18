import logging

import pandas as pd
from dash import Input, Output, dash_table, html

from components import ids
from components.constants import CATEGORIES_DF, DUCKDB_PATH

# from dash.exceptions import PreventUpdate
from functions.data_operations import reshape_by_type
from functions.query_duckdb import construct_query, query_duckdb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register(app):
    @app.callback(
        Output(ids.STORED_DATA, "data"),
        [
            Input(ids.MAP_MODE, "value"),
            Input(ids.TYPE_DROPDOWN, "value"),
            Input(ids.YEAR_SLIDER, "value"),
            Input(ids.DONORTYPE_DROPDOWN, "value"),
            Input(ids.CATEGORIES_DROPDOWN, "value"),
            Input(ids.CATEGORIES_SUB_DROPDOWN, "value"),
        ],
        prevent_initial_call=True,
    )
    def update_stored_data(
        map_mode,
        selected_type,
        selected_years,
        selected_donor_types,
        selected_categories,
        selected_subcategories,
    ):
        """Reads, subsets and stores data based on the set UI inputs.

        Args:
            selected_type (str): Either 'donors' or 'recipients'
            selected_years (list): A list of two integers representing the selected year range.

        Returns:
            list(dict): The stored data as a list of dictionaries.
        """
        query = construct_query(
            selected_years=selected_years,
            selected_categories=selected_categories,
            selected_subcategories=selected_subcategories,
            selected_donor_types=selected_donor_types,
        )

        df_queried = query_duckdb(
            duckdb_db=DUCKDB_PATH,
            query=query,
        )
        df_reshaped = reshape_by_type(df_queried, selected_type)
        # TODO: aggregate before storing?

        # return the filtered data as a list of dicts for storage
        return df_reshaped.to_dict("records")

    @app.callback(
        Output(ids.CATEGORIES_SUB_DROPDOWN, "options"),
        Input(ids.CATEGORIES_DROPDOWN, "value"),
        prevent_initial_call=True,
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
            Input(ids.CATEGORIES_DROPDOWN, "value"),
            Input(ids.CATEGORIES_SUB_DROPDOWN, "value"),
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.STORED_DATA, "data"),
        ],
        prevent_initial_call=True,
    )
    def build_datatable(
        selected_categories,
        selected_subcategories,
        click_data=None,
        stored_data=None,
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
            df_stored = pd.DataFrame(stored_data)

            # filter the data based on the selected categories
            # TODO: is this needed or can we just use the queried data?
            try:
                if selected_subcategories:
                    df_filtered = df_stored[
                        (df_stored["CountryCode"] == country_code)
                        & (df_stored["climate_class"].isin(selected_subcategories))
                    ]
                else:
                    df_filtered = df_stored[
                        (df_stored["CountryCode"] == country_code)
                        & (df_stored["meta_category"].isin(selected_categories))
                    ]
            # this is needed to circumvent an error where filtering on a country
            # that has no data available for the selected categories and years
            # leads to a KeyError
            except KeyError:
                return header + [html.H4("No data available for this country.")]

            if len(df_filtered) == 0:
                return header + [html.H4("No data available for this country.")]
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
        Output(ids.DATATABLE_CARD, "style"),
        Input(ids.MAP_MODE, "value"),
    )
    def toggle_table_visibility(map_mode):
        if map_mode == "base":
            return {"display": "none"}  # Hide the table
        return {"display": "block"}  # Show the table
