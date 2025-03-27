import logging
import time

import dash_bootstrap_components as dbc
import pandas as pd
import pycountry
from dash import Input, Output, html
from flag import flag

from components import flow_data_table, ids
from components.slider_player import PlaybackSliderAIO
from functions.data_operations import aggregate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def iso_to_alpha2(iso_alpha3):
    """Convert ISO Alpha-3 code to Alpha-2 code."""
    try:
        country = pycountry.countries.get(alpha_3=iso_alpha3)
        return (
            country.alpha_2 if country else iso_alpha3
        )  # Return Alpha-2 if found, else fallback to Alpha-3
    except KeyError:
        return iso_alpha3  # In case the code is invalid, return the original code


def get_country_flag(iso_code):
    # Convert ISO Alpha-3 to Alpha-2
    iso_alpha2 = iso_to_alpha2(iso_code)
    try:
        return flag(iso_alpha2)  # Return the flag emoji for the Alpha-2 code
    except KeyError:
        return "🏳️"  # Return default flag if the ISO code is invalid or unsupported


def register(app):
    @app.callback(
        Output(ids.INFOBOX_COUNTRY, "children"),
        [
            Input(ids.MODE_DATA, "data"),
            Input(ids.MAP_MODE, "value"),
            Input(ids.COUNTRIES_LAYER, "hoverData"),
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(ids.STORED_DATA, "data"),
            Input(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER), "value"),
        ],
        prevent_initial_call=True,
    )
    def build_infobox_country(
        mode_data,
        map_mode,
        hover_data=None,
        click_data=None,
        stored_data=None,
        selected_year=None,
    ):
        """Build the infobox for the selected country polygon with adaptation, environment, and mitigation data."""

        start = time.time()
        if not click_data and not hover_data:
            header = [html.H5("🌍 Country Information ℹ️", className="infobox-header")]
            return header + [html.Div("Hover over a country for information.")]

        # Determine which country was selected
        if click_data:
            country_name = click_data["properties"]["name"]
            country_id = click_data["id"]
        else:  # Hover data is available but no click data
            country_name = hover_data["properties"]["name"]
            country_id = hover_data["id"]

        # Get country flag emoji
        country_flag = get_country_flag(country_id)
        header = [html.H5(f"{country_flag} {country_name}", className="infobox-header")]

        try:
            df_mode = pd.DataFrame(mode_data)
            df_subset = df_mode[df_mode["CountryCode"] == country_id]
            df_aggregated = aggregate(df_subset)
            total_value = round(df_aggregated["USD_Disbursement"].iloc[0], 2)

            # Extract adaptation, environment, and mitigation values (already in million USD)
            df_data = pd.DataFrame(stored_data)
            adaptation_value = round(
                df_data[
                    (df_data["meta_category"] == "Adaptation")
                    & (df_data["CountryCode"] == country_id)
                ]["USD_Disbursement"].sum(),
                2,
            )
            environment_value = round(
                df_data[
                    (df_data["meta_category"] == "Environment")
                    & (df_data["CountryCode"] == country_id)
                ]["USD_Disbursement"].sum(),
                2,
            )
            mitigation_value = round(
                df_data[
                    (df_data["meta_category"] == "Mitigation")
                    & (df_data["CountryCode"] == country_id)
                ]["USD_Disbursement"].sum(),
                2,
            )

            end = time.time()
            logger.info(
                f"Execution time for infobox country: {end - start:.2f} seconds"
            )

            # Build the formatted info box
            infobox_components = header + [
                html.Br(),
                html.P(f"🆔 ID: {country_id}"),
                html.Hr(),
                html.P(["⚙️ Adaptation: ", html.B(f"${adaptation_value} Mio USD")]),
                html.P(["🌳 Environment: ", html.B(f"${environment_value} Mio USD")]),
                html.P(["🛡️ Mitigation: ", html.B(f"${mitigation_value} Mio USD")]),
                html.Hr(),
                html.P(
                    ["💰 Total Disbursements: ", html.B(f"${total_value} Mio USD")],
                    className="infobox-total",
                ),
                html.P(f"📅 Year: {selected_year}"),
            ]

            if map_mode != "base" and click_data:
                infobox_components.extend(
                    [
                        html.Div(
                            [
                                dbc.Button(
                                    "🔍 Inspect individual flows",
                                    id=ids.FLOW_DATA_BTN,
                                    n_clicks=0,
                                    className="inspect-btn",
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
                html.P(f"🆔 ID: {country_id}"),
                html.P("❌ No data available."),
            ]
