import pandas as pd
from dash import Dash, Input, Output, dash_table, html

from climatefinancebert_ui.components import ids

test_url = (
    "https://raw.githubusercontent.com/MalteToetzke"
    "/consistent-and-replicable-estimation-of-bilateral-climate-finance"
    "/main/Data/Recipients/recipients.csv"
)

TEST_DATA = pd.read_csv(test_url)


def render(app: Dash):
    @app.callback(
        Output(ids.DATATABLE, "children"),
        [
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.CATEGORIES_DROPDOWN, "value"),
        ],
    )
    def build_datatable(click_data=None, selected_categories=None):
        if not click_data:
            return html.H4("Click a country to render a datatable")
        else:
            country_code = click_data["id"]
            country_name = click_data["properties"]["name"]

            header = [html.H4(f"Data for {country_name}:")]

            filtered_df = TEST_DATA[
                (TEST_DATA["country_code"] == country_code)
                & (TEST_DATA["meta_category"].isin(selected_categories))
            ]

            if len(filtered_df.index) == 0:
                return header + [html.P("No data available")]
            else:
                # Render a DataTable with the filtered data
                return header + [
                    dash_table.DataTable(
                        data=filtered_df.to_dict("records"),
                        columns=[
                            {
                                "name": i,
                                "id": i,
                                # "type": "numeric",
                                # "format": {"specifier": ".2f"},
                            }
                            for i in filtered_df.columns
                        ],
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
