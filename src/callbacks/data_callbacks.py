import logging
import time

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, dash_table, html
from dash.exceptions import PreventUpdate

from components import ids
from components.constants import CATEGORIES_DF, DUCKDB_PATH
from components.widgets.year import PlaybackSliderAIO
from utils.data_operations import create_mode_data, reshape_by_type
from utils.query_duckdb import construct_aggregated_query, construct_query, query_duckdb

logger = logging.getLogger(__name__)


def create_table_from_dataframe(df: pd.DataFrame) -> dash_table.DataTable:
    """Create a formatted data table from a DataFrame.

    Args:
        df: DataFrame containing the data to display

    Returns:
        Formatted DataTable component
    """
    return dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=15,
        sort_action="native",
        style_cell={
            "overflow": "hidden",
            "textOverflow": "ellipsis",
            "maxWidth": 0,
        },
    )


def build_country_data_header(country_name: str) -> list[html.H4]:
    """Create a header for country data displays.

    Args:
        country_name: Name of the country to show in the header

    Returns:
        List containing header components
    """
    return [html.H4(f"Data for {country_name}:")]


def build_flow_data_header(country_name: str) -> list[html.H4]:
    """Create a header for flow data displays.

    Args:
        country_name: Name of the country to show in the header

    Returns:
        List containing header components
    """
    return [html.H4(f"Flow Data for {country_name}:")]


def filter_country_data(df: pd.DataFrame, country_code: str) -> pd.DataFrame:
    """Filter data for a specific country.

    Args:
        df: DataFrame to filter
        country_code: Country code to filter by

    Returns:
        Filtered DataFrame

    Raises:
        KeyError: If country_code column doesn't exist
    """
    return df[df["CountryCode"] == country_code]


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
        """Update the stored data based on user-selected filters.

        Args:
            selected_type: Either 'donors' or 'recipients'
            selected_year: Selected year for data filtering
            selected_donor_types: Types of donors to include
            selected_categories: Categories to include
            selected_subcategories: Subcategories to include
            selected_flow_types: Types of flows to include

        Returns:
            List of dictionaries containing the filtered data
        """
        start = time.time()
        logger.info(
            f"Updating stored data for year: {selected_year}, type: {selected_type}"
        )

        # Construct and execute query based on selected filters
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

        # Reshape data based on selected view type
        df_reshaped = reshape_by_type(df_queried, selected_type)

        end = time.time()
        logger.info(
            f"Execution time for updating stored data: {end - start:.2f} seconds."
        )

        return df_reshaped.to_dict("records")

    @app.callback(
        Output(ids.MODE_DATA, "data"),
        [
            Input(ids.MAP_MODE, "value"),
            Input(ids.STORED_DATA, "data"),
        ],
        [
            State(ids.CATEGORIES_DROPDOWN, "value"),
            State(ids.CATEGORIES_SUB_DROPDOWN, "value"),
        ],
        prevent_initial_call=True,
    )
    def update_mode_data(
        map_mode,
        stored_data,
        selected_categories,
        selected_subcategories,
    ):
        """Update the mode-specific data based on the selected map mode.

        Args:
            map_mode: Selected map visualization mode
            stored_data: Base data from storage
            selected_categories: Selected categories
            selected_subcategories: Selected subcategories

        Returns:
            List of dictionaries with mode-specific data, or empty list for base mode
        """
        # Skip processing for base mode
        if map_mode == "base":
            return []

        logger.info(f"Updating mode data for map mode: {map_mode}")

        # Convert stored data to DataFrame and create mode-specific data
        df = pd.DataFrame(stored_data)
        df_mode = create_mode_data(
            df,
            map_mode,
            selected_categories,
            selected_subcategories,
        )

        return df_mode.to_dict("records")

    @app.callback(
        Output(ids.CATEGORIES_SUB_DROPDOWN, "options"),
        Input(ids.CATEGORIES_DROPDOWN, "value"),
        prevent_initial_call=False,
    )
    def set_meta_options(selected_climate_class):
        """Update subcategory options based on selected categories.

        Args:
            selected_climate_class: Selected climate classes/categories

        Returns:
            List of available subcategory options
        """
        # Filter available meta categories based on selected climate classes
        filtered_df = CATEGORIES_DF[
            CATEGORIES_DF["climate_class"].isin(selected_climate_class)
        ]

        return [{"label": i, "value": i} for i in filtered_df["meta_category"].unique()]

    @app.callback(
        Output(ids.DATATABLE, "children"),
        [
            Input(ids.COUNTRIES_LAYER, "clickData"),
        ],
        [
            State(ids.MODE_DATA, "data"),
        ],
    )
    def build_datatable(
        click_data,
        mode_data,
    ):
        """Build a data table for the selected country.

        Args:
            click_data: Data from the clicked country on the map
            mode_data: Current mode-specific data

        Returns:
            Data table component or message if no data available
        """
        # Check if a country has been selected
        if not click_data:
            return html.H4("Click a country to render a datatable")

        try:
            # Extract country information
            country_name = click_data["properties"]["name"]
            country_code = click_data["id"]

            # Create header for the country
            header = build_country_data_header(country_name)

            # Filter data for selected country
            df_mode = pd.DataFrame(mode_data)
            df_filtered = filter_country_data(df_mode, country_code)

            # Return appropriate content based on data availability
            if df_filtered.empty:
                return header + [
                    html.H4(
                        "No data available for this country for the selected filters."
                    )
                ]
            else:
                return header + [create_table_from_dataframe(df_filtered)]

        except KeyError:
            # Handle case where country has no data
            return header + [html.H4("No data available for this country.")]

    @app.callback(
        Output(ids.FLOW_DATA_TABLE, "children"),
        [
            Input(ids.FLOW_DATA_MODAL, "is_open"),
        ],
        [
            State(ids.COUNTRIES_LAYER, "clickData"),
            State(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER), "value"),
            State(ids.CATEGORIES_DROPDOWN, "value"),
            State(ids.CATEGORIES_SUB_DROPDOWN, "value"),
            State(ids.DONORTYPE_DROPDOWN, "value"),
            State(ids.FLOW_TYPE_DROPDOWN, "value"),
            State(ids.TYPE_DROPDOWN, "value"),
        ],
        prevent_initial_call=True,
    )
    def build_flow_data_table(
        is_open,
        click_data,
        selected_year,
        selected_categories,
        selected_subcategories,
        selected_donor_types,
        selected_flow_types,
        selected_type,
    ):
        """Build a detailed flow data table for the selected country.

        Args:
            is_open: Whether the flow data modal is open
            click_data: Data from the clicked country on the map
            selected_year: Selected year for data filtering
            selected_categories: Categories to include
            selected_subcategories: Subcategories to include
            selected_donor_types: Types of donors to include
            selected_flow_types: Types of flows to include
            selected_type: Either 'donors' or 'recipients'

        Returns:
            Modal content with flow data table

        Raises:
            PreventUpdate: If modal is not open
        """
        # Skip update if modal is not open
        if not is_open:
            raise PreventUpdate

        start = time.time()

        try:
            # Extract country information
            country_name = click_data["properties"]["name"]
            country_code = click_data["id"]

            # Create header for the flow data
            header = build_flow_data_header(country_name)

            # Query aggregated data
            query = construct_aggregated_query(
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

            # Filter for selected country based on view type
            if selected_type == "donors":
                df_filtered = df_queried[df_queried["DEDonorcode"] == country_code]
            else:
                df_filtered = df_queried[df_queried["DERecipientcode"] == country_code]

            # Handle case with no available data
            if df_filtered.empty:
                return [
                    dbc.ModalHeader(dbc.ModalTitle(header)),
                    dbc.ModalBody(
                        html.H4("No data available for the selected filters.")
                    ),
                    dbc.ModalFooter(),
                ]

            end = time.time()
            logger.info(
                f"Execution time for building flow data table: {end - start:.2f} seconds."
            )

            # Return complete modal content with data table
            return [
                dbc.ModalHeader(dbc.ModalTitle(header)),
                dbc.ModalBody(create_table_from_dataframe(df_filtered)),
                dbc.ModalFooter(),
            ]

        except (TypeError, KeyError):
            # Handle invalid country selection
            return [
                dbc.ModalHeader(dbc.ModalTitle("Error")),
                dbc.ModalBody(html.H4("Invalid country selection.")),
                dbc.ModalFooter(),
            ]

    @app.callback(
        Output(ids.DATATABLE_CARD, "style"),
        Input(ids.MAP_MODE, "value"),
    )
    def toggle_table_visibility(map_mode):
        """Toggle visibility of the data table based on map mode.

        Args:
            map_mode: Current map visualization mode

        Returns:
            Style dictionary controlling visibility
        """
        return {"display": "none" if map_mode == "base" else "block"}
