from dash import Dash, Input, Output, dash_table, html

from climatefinancebert_ui.components import ids, utils


def render(app: Dash):
    @app.callback(
        Output(ids.DATATABLE, "children"),
        [
            Input(ids.TYPE_DROPDOWN, "value"),
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.CATEGORIES_DROPDOWN, "value"),
            Input(ids.YEAR_SLIDER, "value"),
        ],
    )
    def build_datatable(
        selected_type=None,
        click_data=None,
        selected_categories=None,
        selected_years=None,
    ):
        """
        Build the datatable based on the input elements and
        the selected map element.
        """

        df_full = utils.fetch_data(selected_type)

        if not click_data:
            return html.H4("Click a country to render a datatable")
        else:
            country_code = click_data["id"]
            country_name = click_data["properties"]["name"]

            header = [html.H4(f"Data for {country_name}:")]

            df_filtered = df_full[
                (df_full["country_code"] == country_code)
                & (df_full["meta_category"].isin(selected_categories))
                & (
                    df_full["effective_year"].between(
                        selected_years[0], selected_years[1]
                    )
                )
            ]

            if len(df_filtered.index) == 0:
                return header + [html.P("No data available")]
            else:
                # Render a DataTable with the filtered data
                return header + [
                    dash_table.DataTable(
                        data=df_filtered.to_dict("records"),
                        columns=[
                            {
                                "name": i,
                                "id": i,
                                # TODO: style datatable values
                                # "type": "numeric",
                                # "format": {"specifier": ".2f"},
                            }
                            for i in df_filtered.columns
                        ],
                        page_size=15,
                        sort_action="native",
                        style_cell={
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "maxWidth": 0,
                        },
                    )
                ]

    return html.Div(
        children=build_datatable(),
        id=ids.DATATABLE,
        className=ids.DATATABLE,
    )
