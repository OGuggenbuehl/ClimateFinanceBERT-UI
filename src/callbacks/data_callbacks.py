import logging

import pandas as pd
from components import ids
from components.constants import CATEGORIES_DF, DUCKDB_PATH
from dash import Input, Output, dash_table, html
from functions.data_operations import reshape_by_type
from functions.query_duckdb import query_duckdb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register(app):
    @app.callback(
        Output(ids.STORED_DATA, "data"),
        [
            Input(ids.TYPE_DROPDOWN, "value"),
            Input(ids.YEAR_SLIDER, "value"),
            Input(ids.DONORTYPE_DROPDOWN, "value"),
            Input(ids.CATEGORIES_DROPDOWN, "value"),
            Input(ids.CATEGORIES_SUB_DROPDOWN, "value"),
            # TODO: find out how to implement categories filters into map coloring
            # Input(ids.CATEGORIES_DROPDOWN, "value"),
            # Input(ids.CATEGORIES_SUB_DROPDOWN, "value"),
        ],
    )
    def update_stored_data(
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

        # Construct SQL query
        query = f"""
        SELECT *
        FROM my_table
        WHERE Year BETWEEN {selected_years[0]} AND {selected_years[1]}
        """

        # construct type filter query if selected
        if selected_categories:
            if isinstance(selected_categories, list):
                category_list = ",".join(f"'{cat}'" for cat in selected_categories)
                query += f"AND meta_category IN ({category_list})"
            else:
                query += f"AND meta_category = '{selected_categories}'"

        # construct subcategory filter query if selected
        if selected_subcategories:
            if isinstance(selected_subcategories, list):
                subcategory_list = ",".join(
                    f"'{sub}'" for sub in selected_subcategories
                )
                query += f" AND climate_class IN ({subcategory_list})"
            else:
                query += f" AND climate_class = '{selected_subcategories}'"

        # construct donor type filter query if selected
        if selected_donor_types:
            if isinstance(selected_donor_types, list):
                formatted_donor_types = tuple(
                    donor_type for donor_type in selected_donor_types
                )
                query += f" AND DonorType IN {formatted_donor_types};"
            else:
                query += f" AND DonorType = '{selected_donor_types}';"

        df_filtered = query_duckdb(
            duckdb_db=DUCKDB_PATH,
            query=query,
        )
        df_reshaped = reshape_by_type(df_filtered, selected_type)

        # return the filtered data as a list of  for storage
        return df_reshaped.to_dict("records")

    @app.callback(
        Output(ids.CATEGORIES_SUB_DROPDOWN, "options"),
        Input(ids.CATEGORIES_DROPDOWN, "value"),
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
    )
    def build_datatable(
        selected_categories,
        selected_subcategories,
        click_data=None,
        stored_data=None,
    ):
        """
        Build the datatable based on the input elements and
        the selected map element.
        """
        # TODO: Bugfix when no data is available
        if not click_data:
            return html.H4("Click a country to render a datatable")
        else:
            # build the info header based on the clicked country
            country_name = click_data["properties"]["name"]
            header = [html.H4(f"Data for {country_name}:")]

            # subset the data based on the selected country
            country_code = click_data["id"]
            df_stored = pd.DataFrame(stored_data)

            # Filter the data based on the selected categories
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
                # Render a DataTable with the filtered data
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
