import pandas as pd
from components import ids
from components.slider_player import PlaybackSliderAIO
from dash import Input, Output, html


def register(app):
    @app.callback(
        Output(ids.INFOBOX_COUNTRY, "children"),
        [
            Input(ids.STORED_DATA, "data"),
            Input(ids.MAP_MODE, "value"),
            Input(ids.COUNTRIES_LAYER, "hoverData"),
            Input(ids.COUNTRIES_LAYER, "clickData"),
        ],
    )
    def build_infobox_country(
        stored_data,
        map_mode_value,
        hover_data=None,
        click_data=None,
    ):
        # TODO: Add docstring
        if not click_data and not hover_data:
            header = [html.H5("Country Information")]
            if map_mode_value == "base":
                return header + [
                    html.Div("Hover over a country for information."),
                ]
            elif map_mode_value == "total":
                return header + [
                    html.Div("Hover over a country for information."),
                    html.Div("Click on a country to zoom in."),
                ]

        if click_data:
            country_name = click_data["properties"]["name"]
            country_id = click_data["id"]
        elif hover_data and not click_data:
            country_name = hover_data["properties"][
                "name"
            ]  # Fixed to access 'properties'
            country_id = hover_data["id"]

        header = [html.H5(country_name)]
        try:
            stored_df = pd.DataFrame(stored_data)
            df_subset = stored_df[stored_df["CountryCode"] == country_id]
            value = df_subset["gdp"].iloc[0]

            return header + [
                html.Br(),
                html.P(f"ID: {country_id}"),
                html.P(f"GDP: {value.round(2)}"),
            ]
        except (IndexError, KeyError):
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
    )
    def build_infobox_adaptation(
        click_data,
        stored_data=None,
        selected_year=None,
    ):
        data = pd.DataFrame(stored_data)
        header = [html.H5("Adaptation")]

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

        # Calculate the total volume of effective funding for the selected category
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

        # If there is no data available for the selected timespan, add a message to the infobox
        if "No data available for this timespan." in infobox_components:
            infobox_components.append(html.P("No data available for this timespan."))

        # Return the header and the infobox components
        return header + infobox_components

    @app.callback(
        Output(ids.INFOBOX_ENVIRONMENT, "children"),
        [
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.STORED_DATA, "data"),
            Input(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER), "value"),
        ],
    )
    def build_infobox_environment(
        click_data,
        stored_data=None,
        selected_year=None,
    ):
        data = pd.DataFrame(stored_data)
        header = [html.H5("Environment")]

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

        # Calculate the total volume of effective funding for the selected category
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

        # If there is no data available for the selected timespan, add a message to the infobox
        if "No data available for this timespan." in infobox_components:
            infobox_components.append(html.P("No data available for this timespan."))

        # Return the header and the infobox components
        return header + infobox_components

    @app.callback(
        Output(ids.INFOBOX_MITIGATION, "children"),
        [
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.STORED_DATA, "data"),
            Input(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER), "value"),
        ],
    )
    def build_infobox_mitigation(
        click_data,
        stored_data=None,
        selected_year=None,
    ):
        data = pd.DataFrame(stored_data)
        header = [html.H5("Mitigation")]

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

        # Calculate the total volume of effective funding for the selected category
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

        # If there is no data available for the selected timespan, add a message to the infobox
        if "No data available for this timespan." in infobox_components:
            infobox_components.append(html.P("No data available for this timespan."))

        # Return the header and the infobox components
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
