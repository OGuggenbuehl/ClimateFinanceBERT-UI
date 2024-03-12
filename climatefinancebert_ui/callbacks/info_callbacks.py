import pandas as pd
from dash import Input, Output, html

from climatefinancebert_ui.components import ids


def register(app):
    @app.callback(
        Output(ids.INFOBOX_COUNTRY, "children"),
        Input(ids.COUNTRIES_LAYER, "hoverData"),
    )
    def build_infobox_country(hover_data=None):
        # TODO: Add docstring
        header = [html.H5("Country Information")]
        if not hover_data:
            return header + [html.P("Hover over a country")]
        country_name = hover_data["properties"]["name"]  # Fixed to access 'properties'
        return header + [
            html.B(country_name),
            html.Br(),
            html.P(f"its ID is: {hover_data['id']}"),
        ]

    @app.callback(
        Output(ids.INFOBOX_ADAPTATION, "children"),
        Input(ids.YEAR_SLIDER, "value"),
    )
    def build_infobox_adaptation(year=None):
        header = [html.H5("Adaptation Information")]
        if not year:
            return header + [html.P("Select a year")]
        # Ensure a range is provided for the year
        year_range = f"{year[0]} - {year[1]}" if isinstance(year, list) else year
        return header + [
            html.P(f"Showing data from {year_range}"),
        ]

    @app.callback(
        Output(ids.INFOBOX_CLIMATEFINANCE, "children"),
        [
            Input(ids.YEAR_SLIDER, "value"),
            Input(ids.STORED_DATA, "data"),
        ],
    )
    def build_infobox_climatefinance(
        year=None,
        stored_data=None,
    ):
        data = pd.DataFrame(stored_data)
        header = [html.H5("Climate-Finance Information")]
        if not year:
            return header + [html.P("Select a year")]
        return header + [
            html.P(f"Showing data from {year[0]} - {year[1]}"),
            html.P(f"data has length: {len(data)}"),
        ]

    @app.callback(
        Output(ids.INFOBOX_ENVIRONMENT, "children"),
        Input(ids.YEAR_SLIDER, "value"),
    )
    def build_infobox_environment(year=None):
        header = [html.H5("Environment Information")]
        if not year:
            return header + [html.P("Select a year")]
        return header + [
            html.P(f"Showing data from {year[0]} - {year[1]}"),
        ]

    @app.callback(
        Output(ids.INFOBOX_MITIGATION, "children"),
        Input(ids.YEAR_SLIDER, "value"),
    )
    def build_infobox_mitigation(year=None):
        header = [html.H5("Mitigation Information")]
        if not year:
            return header + [html.P("Select a year")]
        return header + [
            html.P(f"Showing data from {year[0]} - {year[1]}"),
        ]
