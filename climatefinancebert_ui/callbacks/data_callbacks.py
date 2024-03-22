import pandas as pd
from dash import Input, Output, dash_table, html

from climatefinancebert_ui.components import ids, utils


def register(app):
    @app.callback(
        Output(ids.STORED_DATA, "data"),
        [
            Input(ids.TYPE_DROPDOWN, "value"),
            Input(ids.YEAR_SLIDER, "value"),
        ],
    )
    def update_stored_data(
        selected_type,
        selected_years,
    ):
        # TODO: Add docstring
        df_full = utils.fetch_data(selected_type)

        df_filtered = df_full[
            (df_full["effective_year"].between(selected_years[0], selected_years[1]))
        ]

        return df_filtered.to_dict("records")

    @app.callback(
        Output(ids.DATATABLE, "children"),
        [
            Input(ids.CATEGORIES_DROPDOWN, "value"),
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.STORED_DATA, "data"),
        ],
    )
    def build_datatable(
        selected_categories,
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
            # build the info header based on the hovered over country
            country_name = click_data["properties"]["name"]
            header = [html.H4(f"Data for {country_name}:")]

            # subset the data based on the selected country
            country_code = click_data["id"]
            df_stored = pd.DataFrame(stored_data)

            # Filter the data based on the selected categories
            try:
                df_filtered = df_stored[
                    (df_stored["country_code"] == country_code)
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
