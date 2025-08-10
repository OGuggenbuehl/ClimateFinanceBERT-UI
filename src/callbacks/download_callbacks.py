import logging
from typing import Any, Optional

import pandas as pd
from dash import Input, Output, State, callback_context, dash_table, dcc, html
from dash.exceptions import PreventUpdate

from components import ids
from components.constants import DUCKDB_PATH
from utils.query_duckdb import construct_query, query_duckdb

logger = logging.getLogger(__name__)


def register(app):
    """
    Register download-related callbacks with the Dash application.

    Args:
        app: The Dash application instance
    """

    @app.callback(
        Output(ids.DOWNLOAD_QUERIED_DATA, "data"),
        [
            Input(ids.QUERY_BTN, "n_clicks"),
            Input(ids.YEAR_SLIDER_DOWNLOAD, "value"),
            Input(ids.CATEGORIES_DROPDOWN_DOWNLOAD, "value"),
            Input(ids.CATEGORIES_SUB_DROPDOWN_DOWNLOAD, "value"),
            Input(ids.DONORTYPE_DROPDOWN_DOWNLOAD, "value"),
            Input(ids.FLOW_TYPE_DROPDOWN_DOWNLOAD, "value"),
        ],
        prevent_initial_call=True,
    )
    def pull_data(
        n_clicks: int,
        selected_years: list[int],
        selected_categories: list[str],
        selected_subcategories: list[str],
        selected_donor_types: list[str],
        selected_flow_types: list[str],
    ) -> list[dict[str, Any]]:
        """
        Pull data from the database based on user-selected filters.

        Args:
            n_clicks: Number of times the query button was clicked
            selected_years: Range of years selected by the user
            selected_categories: list of climate categories selected by the user
            selected_subcategories: list of subcategories selected by the user
            selected_donor_types: list of donor types selected by the user
            selected_flow_types: list of flow types selected by the user

        Returns:
            list of dictionaries representing table records

        Raises:
            PreventUpdate: If the callback wasn't triggered by clicking the query button
        """
        if not _is_query_button_clicked():
            raise PreventUpdate

        logger.info("Query Button clicked: Pulling data")

        # Construct and execute query
        query = _build_query(
            selected_years,
            selected_categories,
            selected_subcategories,
            selected_donor_types,
            selected_flow_types,
        )

        queried_df = _execute_query(query)

        return queried_df.to_dict("records")

    @app.callback(
        Output(ids.DOWNLOAD_DATATABLE, "children"),
        [Input(ids.DOWNLOAD_QUERIED_DATA, "data")],
        prevent_initial_call=True,
    )
    def build_download_datatable(
        queried_data: Optional[list[dict[str, Any]]] = None,
    ) -> html.H3 | list[dash_table.DataTable]:
        """
        Build a data table display from the queried data.

        Args:
            queried_data: The data to display in the table, as a list of dict records

        Returns:
            Either an error message if no data is available, or a DataTable component
        """
        df_table = pd.DataFrame(queried_data).drop(
            columns=["labelled_bilateral"], errors="ignore"
        )

        if len(df_table) == 0:
            return html.H3("No data available for the selected filters.")

        return [_create_data_table(df_table)]

    @app.callback(
        Output(ids.DOWNLOAD_TRIGGER, "data"),
        [Input(ids.DOWNLOAD_BTN, "n_clicks")],
        [
            State(ids.DOWNLOAD_QUERIED_DATA, "data"),
            State(ids.YEAR_SLIDER_DOWNLOAD, "value"),
        ],
        prevent_initial_call=True,
    )
    def download_csv(
        n_clicks: int,
        queried_data: Optional[list[dict[str, Any]]],
        selected_years: list[int],
    ) -> dcc.send_data_frame:
        """
        Create a CSV download of the queried data.

        Args:
            n_clicks: Number of times the download button was clicked
            queried_data: The data to be downloaded as CSV
            selected_years: The year range for the filename

        Returns:
            A send_data_frame object that triggers a file download

        Raises:
            PreventUpdate: If the download button wasn't clicked or no data is available
        """
        if not n_clicks or not queried_data:
            raise PreventUpdate

        logger.info("downloading queried data as CSV")
        filename = _generate_filename(selected_years)

        return dcc.send_data_frame(
            pd.DataFrame(queried_data).to_csv,
            filename,
            index=False,
        )

    @app.callback(
        Output(ids.DATATABLE_CARD_DOWNLOAD, "style"),
        Input(ids.QUERY_BTN, "n_clicks"),
    )
    def toggle_download_table_visibility(queried: int) -> dict[str, str]:
        """
        Toggle the visibility of the data table based on whether a query has been executed.

        Args:
            queried: Number of times the query button was clicked

        Returns:
            CSS style dictionary controlling the display property
        """
        return {"display": "none"} if not queried else {"display": "block"}


def _is_query_button_clicked() -> bool:
    """
    Check if the callback was triggered by clicking the query button.

    Returns:
        True if the query button was clicked, False otherwise
    """
    ctx = callback_context
    return ctx.triggered and ctx.triggered[0]["prop_id"].split(".")[0] == ids.QUERY_BTN


def _build_query(
    selected_years: list[int],
    selected_categories: list[str],
    selected_subcategories: list[str],
    selected_donor_types: list[str],
    selected_flow_types: list[str],
) -> str:
    """
    Build a database query based on the selected filters.

    Args:
        selected_years: Range of years selected by the user
        selected_categories: list of climate categories selected by the user
        selected_subcategories: list of subcategories selected by the user
        selected_donor_types: list of donor types selected by the user
        selected_flow_types: list of flow types selected by the user

    Returns:
        SQL query string for the DuckDB database
    """
    return construct_query(
        year_type="timespan",
        selected_year=selected_years,
        selected_categories=selected_categories,
        selected_subcategories=selected_subcategories,
        selected_donor_types=selected_donor_types,
        selected_flow_types=selected_flow_types,
    )


def _execute_query(query: str) -> pd.DataFrame:
    """
    Execute a query against the DuckDB database.

    Args:
        query: SQL query string

    Returns:
        DataFrame containing the query results
    """
    return query_duckdb(
        duckdb_db=DUCKDB_PATH,
        query=query,
    )


def _create_data_table(df: pd.DataFrame) -> dash_table.DataTable:
    """
    Create a Dash DataTable component from a DataFrame.

    Args:
        df: DataFrame with the data to display

    Returns:
        A configured DataTable component
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


def _generate_filename(selected_years: list[int]) -> str:
    """
    Generate a filename for the CSV download based on the selected years.

    Args:
        selected_years: The year range to include in the filename

    Returns:
        A formatted filename string
    """
    return f"ClimFinBERT_data_{selected_years[0]}-{selected_years[1]}.csv"
