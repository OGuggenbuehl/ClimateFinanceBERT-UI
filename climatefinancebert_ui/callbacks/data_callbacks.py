import pandas as pd
from dash import Input, Output, dash_table, html

from climatefinancebert_ui.components import ids, utils


def register(app):
    @app.callback(
        Output(ids.STORED_DATA, "data"),
        [
            Input(ids.TYPE_DROPDOWN, "value"),
            Input(ids.CATEGORIES_DROPDOWN, "value"),
            Input(ids.YEAR_SLIDER, "value"),
            Input(ids.COUNTRIES_LAYER, "clickData"),
        ],
    )
    def update_stored_data(
        selected_type,
        selected_categories,
        selected_years,
        click_data=None,
    ):
        # TODO: Add docstring
        country_code = click_data["id"] if click_data else None

        df_full = utils.fetch_data(selected_type)

        df_filtered = df_full[
            (df_full["country_code"] == country_code)
            & (df_full["meta_category"].isin(selected_categories))
            & (df_full["effective_year"].between(selected_years[0], selected_years[1]))
        ]

        return df_filtered.to_dict("records")

    @app.callback(
        Output(ids.DATATABLE, "children"),
        [
            Input("stored-data", "data"),
            Input(ids.COUNTRIES_LAYER, "clickData"),
        ],
    )
    def build_datatable(stored_data=None, click_data=None):
        """
        Build the datatable based on the input elements and
        the selected map element.
        """
        if not click_data or not stored_data:
            return html.H4("Click a country to render a datatable")
        else:
            country_name = click_data["properties"]["name"]
            header = [html.H4(f"Data for {country_name}:")]
            df_filtered = pd.DataFrame(stored_data)

            if len(df_filtered.index) == 0:
                return header + [html.P("No data available")]
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
