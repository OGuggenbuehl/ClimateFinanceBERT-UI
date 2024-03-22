import pandas as pd
from dash import Input, Output, html

from climatefinancebert_ui.components import ids


def register(app):
    @app.callback(
        Output(ids.INFOBOX_COUNTRY, "children"),
        [
            Input(ids.STORED_DATA, "data"),
            Input(ids.COUNTRIES_LAYER, "hoverData"),
        ],
    )
    def build_infobox_country(
        stored_data,
        hover_data=None,
    ):
        # TODO: Add docstring
        if not hover_data:
            header = [html.H5("Country Information")]
            return header + [html.P("Hover over a country")]

        country_name = hover_data["properties"]["name"]  # Fixed to access 'properties'
        country_id = hover_data["id"]

        header = [html.H5(country_name)]
        try:
            stored_data = pd.DataFrame(stored_data)
            df_subset = stored_data[stored_data["country_code"] == country_id]
            value = df_subset["gdp"].iloc[0]

            return header + [
                html.Br(),
                html.P(f"ID: {hover_data['id']}"),
                html.P(f"GDP: {value.round(2)}"),
            ]
        except IndexError:
            return header + [
                html.Br(),
                html.P(f"ID: {hover_data['id']}"),
            ]

    @app.callback(
        Output(ids.INFOBOX_ADAPTATION, "children"),
        [
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.STORED_DATA, "data"),
        ],
    )
    def build_infobox_adaptation(
        click_data,
        stored_data=None,
    ):
        data = pd.DataFrame(stored_data)
        header = [html.H5("Adaptation Information")]

        if click_data is not None:
            country_code = click_data["id"]
            df_filtered = data[
                (data["meta_category"].isin(["Adaptation"]))
                & (data["country_code"] == country_code)
            ]
        else:
            df_filtered = data[(data["meta_category"].isin(["Adaptation"]))]

        volume = df_filtered.effective_funding.sum().round(2)

        return header + [html.P(f"Volume: {volume}")]

    @app.callback(
        Output(ids.INFOBOX_CLIMATEFINANCE, "children"),
        [
            Input(ids.YEAR_SLIDER, "value"),
            Input(ids.STORED_DATA, "data"),
        ],
    )
    def build_infobox_climatefinance(
        click_data,
        stored_data=None,
    ):
        # data = pd.DataFrame(stored_data)
        header = [html.H5("ClimateFinance Information")]

        # if click_data is not None:
        #     country_code = click_data["id"]
        #     df_filtered = data[
        #         (data["meta_category"].isin(["Mitigation"]))
        #         & (data["country_code"] == country_code)
        #     ]
        # else:
        #     df_filtered = data[(data["meta_category"].isin(["Mitigation"]))]

        # volume = df_filtered.effective_funding.sum().round(2)

        # return header + [html.P(f"Volume: {volume}")]
        return header + [html.P("There seems to be no data for ClimateFinance.")]

    @app.callback(
        Output(ids.INFOBOX_ENVIRONMENT, "children"),
        [
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.STORED_DATA, "data"),
        ],
    )
    def build_infobox_environment(
        click_data,
        stored_data=None,
    ):
        data = pd.DataFrame(stored_data)
        header = [html.H5("Environment Information")]

        if click_data is not None:
            country_code = click_data["id"]
            df_filtered = data[
                (data["meta_category"].isin(["Environment"]))
                & (data["country_code"] == country_code)
            ]
        else:
            df_filtered = data[(data["meta_category"].isin(["Environment"]))]

        volume = df_filtered.effective_funding.sum().round(2)

        return header + [html.P(f"Volume: {volume}")]

    @app.callback(
        Output(ids.INFOBOX_MITIGATION, "children"),
        [
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.STORED_DATA, "data"),
        ],
    )
    def build_infobox_mitigation(
        click_data,
        stored_data=None,
    ):
        data = pd.DataFrame(stored_data)
        header = [html.H5("Mitigation Information")]

        if click_data is not None:
            country_code = click_data["id"]
            df_filtered = data[
                (data["meta_category"].isin(["Mitigation"]))
                & (data["country_code"] == country_code)
            ]
        else:
            df_filtered = data[(data["meta_category"].isin(["Mitigation"]))]

        volume = df_filtered.effective_funding.sum().round(2)

        return header + [html.P(f"Volume: {volume}")]
