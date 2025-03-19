import logging
import time

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, html

from components import flow_data_table, ids
from components.slider_player import PlaybackSliderAIO
from functions.data_operations import aggregate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def register(app):
    @app.callback(
        Output(ids.INFOBOX_COUNTRY, "children"),
        [
            Input(ids.MODE_DATA, "data"),
            Input(ids.MAP_MODE, "value"),
            Input(ids.COUNTRIES_LAYER, "hoverData"),
            Input(ids.COUNTRIES_LAYER, "clickData"),
        ],
        prevent_initial_call=True,
    )
    def build_infobox_country(
        mode_data,
        map_mode,
        hover_data=None,
        click_data=None,
    ):
        """Build the infobox for the selected country polygon.

        Args:
            stored_data (dict): The stored data from the data query.
            map_mode (str): The selected map mode.
            hover_data (dict, optional): The hover data from the countries layer. Defaults to None.
            click_data (_type_, optional): The click data from the countries layer. Defaults to None.
        Returns:
            html: The infobox for the selected country polygon.
        """
        start = time.time()
        if not click_data and not hover_data:
            header = [html.H5("Country Information ℹ️")]
            if map_mode == "base":
                return header + [
                    html.Div("Hover over a country for information."),
                ]
            else:
                return header + [
                    html.Div("Hover over a country for information."),
                    html.Div("Click on a country to zoom in."),
                ]

        if click_data:
            country_name = click_data["properties"]["name"]
            country_id = click_data["id"]
        elif hover_data and not click_data:
            country_name = hover_data["properties"]["name"]
            country_id = hover_data["id"]

        header = [html.H5(country_name)]
        try:
            df_mode = pd.DataFrame(mode_data)
            df_subset = df_mode[df_mode["CountryCode"] == country_id]
            df_aggregated = aggregate(df_subset)
            value = df_aggregated["USD_Disbursement"].iloc[0]

            end = time.time()
            logger.info(
                f"Execution time for infobox country: {end - start:.2f} seconds"
            )
            infobox_components = header + [
                html.Br(),
                html.P(f"ID: {country_id}"),
                html.P(f"Total Disbursements: ${value.round(2)}"),
            ]

            if map_mode != "base" and click_data:
                infobox_components.extend(
                    [
                        html.Div(
                            [
                                dbc.Button(
                                    "Inspect individual flows",
                                    id=ids.FLOW_DATA_BTN,
                                    n_clicks=0,
                                ),
                                dbc.Modal(
                                    flow_data_table.render(),
                                    id=ids.FLOW_DATA_MODAL,
                                    size="xl",
                                    is_open=False,
                                ),
                            ]
                        )
                    ]
                )

            return infobox_components
        except (IndexError, KeyError):
            end = time.time()
            logger.info(
                f"Execution time for infobox country: {end - start:.2f} seconds"
            )
            return header + [
                html.Br(),
                html.P(f"ID: {country_id}"),
            ]

    @app.callback(
        Output(ids.INFOBOX_ADAPTATION, "children"),
        [
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.STORED_DATA, "data"),
            Input(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER), "value"),
        ],
        prevent_initial_call=True,
    )
    def build_infobox_adaptation(
        click_data,
        stored_data=None,
        selected_year=None,
    ):
        start = time.time()
        data = pd.DataFrame(stored_data)
        header = [html.H5("Adaptation ⚙️")]

        # If a country is clicked, filter the data for that country
        if click_data is not None:
            country_code = click_data["id"]
            country_name = click_data["properties"]["name"]
            try:
                df_filtered = data[
                    (data["meta_category"].isin(["Adaptation"]))
                    & (data["CountryCode"] == country_code)
                ]
            except KeyError:
                return header + [html.P("No data available for this timespan.")]
        # If no country is clicked, filter only for the category
        else:
            try:
                df_filtered = data[(data["meta_category"].isin(["Adaptation"]))]
            except KeyError:
                return header + [html.P("No data available for this timespan.")]

        volume = df_filtered["USD_Disbursement"].sum().round(2)

        # Create a list to store the components of the infobox
        infobox_components = []

        # If a country is clicked, add the country name to the infobox
        if click_data is not None:
            infobox_components.append(html.Div(f"Country: {country_name}"))

        # Add the volume and timespan to the infobox
        infobox_components.extend(
            [
                html.Div(f"Volume: {volume}"),
                html.Div(f"Timespan: {selected_year}"),
            ]
        )

        if "No data available for this timespan." in infobox_components:
            infobox_components.append(html.P("No data available for this timespan."))

        end = time.time()
        logger.info(f"Execution time for infobox adaptation: {end - start:.2f} seconds")
        return header + infobox_components

    @app.callback(
        Output(ids.INFOBOX_ENVIRONMENT, "children"),
        [
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.STORED_DATA, "data"),
            Input(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER), "value"),
        ],
        prevent_initial_call=True,
    )
    def build_infobox_environment(
        click_data,
        stored_data=None,
        selected_year=None,
    ):
        start = time.time()
        data = pd.DataFrame(stored_data)
        header = [html.H5("Environment 🌳")]

        # If a country is clicked, filter the data for that country
        if click_data is not None:
            country_code = click_data["id"]
            country_name = click_data["properties"]["name"]
            try:
                df_filtered = data[
                    (data["meta_category"].isin(["Environment"]))
                    & (data["CountryCode"] == country_code)
                ]
            except KeyError:
                return header + [html.P("No data available for this timespan.")]
        # If no country is clicked, filter only for the category
        else:
            try:
                df_filtered = data[(data["meta_category"].isin(["Environment"]))]
            except KeyError:
                return header + [html.P("No data available for this timespan.")]

        volume = df_filtered["USD_Disbursement"].sum().round(2)

        # Create a list to store the components of the infobox
        infobox_components = []

        # If a country is clicked, add the country name to the infobox
        if click_data is not None:
            infobox_components.append(html.Div(f"Country: {country_name}"))

        # Add the volume and timespan to the infobox
        infobox_components.extend(
            [
                html.Div(f"Volume: {volume}"),
                html.Div(f"Timespan: {selected_year}"),
            ]
        )

        if "No data available for this timespan." in infobox_components:
            infobox_components.append(html.P("No data available for this timespan."))

        end = time.time()
        logger.info(
            f"Execution time for infobox environment: {end - start:.2f} seconds"
        )
        return header + infobox_components

    @app.callback(
        Output(ids.INFOBOX_MITIGATION, "children"),
        [
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.STORED_DATA, "data"),
            Input(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER), "value"),
        ],
        prevent_initial_call=True,
    )
    def build_infobox_mitigation(
        click_data,
        stored_data=None,
        selected_year=None,
    ):
        start = time.time()
        data = pd.DataFrame(stored_data)
        header = [html.H5("Mitigation 🛡️")]

        # If a country is clicked, filter the data for that country
        if click_data is not None:
            country_code = click_data["id"]
            country_name = click_data["properties"]["name"]
            try:
                df_filtered = data[
                    (data["meta_category"].isin(["Mitigation"]))
                    & (data["CountryCode"] == country_code)
                ]
            except KeyError:
                return header + [html.P("No data available for this timespan.")]
        # If no country is clicked, filter only for the category
        else:
            try:
                df_filtered = data[(data["meta_category"].isin(["Mitigation"]))]
            except KeyError:
                return header + [html.P("No data available for this timespan.")]

        volume = df_filtered["USD_Disbursement"].sum().round(2)

        # Create a list to store the components of the infobox
        infobox_components = []

        # If a country is clicked, add the country name to the infobox
        if click_data is not None:
            infobox_components.append(html.Div(f"Country: {country_name}"))

        # Add the volume and timespan to the infobox
        infobox_components.extend(
            [
                html.Div(f"Volume: {volume}"),
                html.Div(f"Timespan: {selected_year}"),
            ]
        )

        if "No data available for this timespan." in infobox_components:
            infobox_components.append(html.P("No data available for this timespan."))

        end = time.time()
        logger.info(f"Execution time for infobox mitigation: {end - start:.2f} seconds")
        return header + infobox_components

    ## CLIMATE FINANCE INFO ##

    # @app.callback(
    #     Output(ids.INFOBOX_CLIMATEFINANCE, "children"),
    #     [
    #         Input(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER), "value"),
    #         Input(ids.STORED_DATA, "data"),
    #     ],
    # )
    # def build_infobox_climatefinance(
    #     click_data,
    #     stored_data=None,
    # ):
    #     # data = pd.DataFrame(stored_data)
    #     header = [html.H5("ClimateFinance")]

    #     if click_data is not None:
    #         country_code = click_data["id"]
    #         df_filtered = data[
    #             (data["meta_category"].isin(["Mitigation"]))
    #             & (data["CountryCode"] == country_code)
    #         ]
    #     else:
    #         df_filtered = data[(data["meta_category"].isin(["Mitigation"]))]

    #     volume = df_filtered.USD_Disbursement.sum().round(2)

    #     # return header + [html.P(f"Volume: {volume}")]
    #     return header + [html.P("No data for ClimateFinance.")]
