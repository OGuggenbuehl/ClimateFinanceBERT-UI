import logging

import pandas as pd
from dash import Input, Output, State, callback_context, dash_table, dcc, html
from dash.exceptions import PreventUpdate

from components import ids
from components.constants import DUCKDB_PATH
from components.slider_player import PlaybackSliderAIO
from functions.query_duckdb import construct_query, query_duckdb

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def register(app):
    @app.callback(
        Output(ids.DOWNLOAD_QUERIED_DATA, "data"),
        [
            Input(ids.QUERY_BTN, "n_clicks"),
            Input(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER_DOWNLOAD), "value"),
            Input(ids.CATEGORIES_DROPDOWN_DOWNLOAD, "value"),
            Input(ids.CATEGORIES_SUB_DROPDOWN_DOWNLOAD, "value"),
            Input(ids.DONORTYPE_DROPDOWN_DOWNLOAD, "value"),
            Input(ids.FLOW_TYPE_DROPDOWN_DOWNLOAD, "value"),
        ],
        prevent_initial_call=True,
    )
    def pull_data(
        n_clicks,
        selected_year,
        selected_categories,
        selected_subcategories,
        selected_donor_types,
        selected_flow_types,
    ):
        # check if the button was clicked
        ctx = callback_context
        if (
            not ctx.triggered
            or ctx.triggered[0]["prop_id"].split(".")[0] != ids.QUERY_BTN
        ):
            raise PreventUpdate

        logger.info("Query Button clicked: Pulling data")

        query = construct_query(
            selected_year=selected_year,
            selected_categories=selected_categories,
            selected_subcategories=selected_subcategories,
            selected_donor_types=selected_donor_types,
            selected_flow_types=selected_flow_types,
        )

        queried_df = query_duckdb(
            duckdb_db=DUCKDB_PATH,
            query=query,
        )

        return queried_df.to_dict("records")

    @app.callback(
        Output(ids.DOWNLOAD_DATATABLE, "children"),
        [Input(ids.DOWNLOAD_QUERIED_DATA, "data")],
        prevent_initial_call=True,
    )
    def build_download_datatable(
        queried_data=None,
    ):
        df_table = pd.DataFrame(queried_data)

        if len(df_table) == 0:
            return html.H3("No data available for the selected filters.")
        else:
            return [
                dash_table.DataTable(
                    data=df_table.to_dict("records"),
                    columns=[{"name": i, "id": i} for i in df_table.columns],
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
        Output(ids.DOWNLOAD_TRIGGER, "data"),
        [Input(ids.DOWNLOAD_BTN, "n_clicks")],
        [State(ids.DOWNLOAD_QUERIED_DATA, "data")],
        prevent_initial_call=True,
    )
    def download_csv(
        n_clicks,
        queried_data,
    ):
        if not n_clicks or not queried_data:
            raise PreventUpdate

        logger.info("downloading queried data as CSV")

        return dcc.send_data_frame(
            pd.DataFrame(queried_data).to_csv,
            "queried_data.csv",
            index=False,
        )

    @app.callback(
        Output(ids.DATATABLE_CARD_DOWNLOAD, "style"),
        Input(ids.QUERY_BTN, "n_clicks"),
    )
    def toggle_table_visibility(queried):
        if not queried:
            return {"display": "none"}  # Hide the table
        return {"display": "block"}  # Show the table
