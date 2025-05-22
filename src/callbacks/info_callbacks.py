import logging
import time
from typing import Any, Optional, Tuple

import dash_bootstrap_components as dbc
import pandas as pd
import pycountry
from dash import Input, Output, State, html
from flag import flag

from components import ids
from components.widgets.year import PlaybackSliderAIO
from utils.data_operations import aggregate

logger = logging.getLogger(__name__)


def iso_to_alpha2(iso_alpha3: str) -> str:
    """Convert ISO Alpha-3 code to Alpha-2 code."""
    try:
        country = pycountry.countries.get(alpha_3=iso_alpha3)
        return country.alpha_2 if country else iso_alpha3
    except KeyError:
        return iso_alpha3


def get_country_flag(iso_code: str) -> str:
    """Return the flag emoji for the given ISO code."""
    iso_alpha2 = iso_to_alpha2(iso_code)
    try:
        return flag(iso_alpha2)
    except KeyError:
        return "🏳️"


def register(app):
    """
    Register info-related callbacks with the Dash application.

    Args:
        app: The Dash application instance
    """

    @app.callback(
        Output(ids.INFOBOX, "children"),
        [
            Input(ids.MAP_MODE, "value"),
            Input(ids.COUNTRIES_LAYER, "hoverData"),
            Input(ids.COUNTRIES_LAYER, "clickData"),
            Input(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER), "value"),
        ],
        [
            State(ids.STORED_DATA, "data"),
            State(ids.MODE_DATA, "data"),
        ],
        prevent_initial_call=True,
    )
    def build_infobox(
        map_mode: str,
        hover_data: Optional[dict],
        click_data: Optional[dict],
        selected_year: int,
        stored_data: list[dict[str, Any]],
        mode_data: list[dict[str, Any]],
    ) -> list[html.H5 | html.Div | html.P | html.Hr | html.Br]:
        """
        Build the infobox for the selected country with climate finance data.

        Args:
            map_mode: The current map visualization mode
            hover_data: Data from hovering over a country
            click_data: Data from clicking on a country
            selected_year: The selected year for data filtering
            stored_data: Stored climate finance data
            mode_data: Mode-specific data for the current map mode

        Returns:
            A list of HTML components forming the infobox
        """
        start = time.time()

        # Handle case when no country is selected
        if not click_data and not hover_data:
            return _create_default_infobox()

        # Extract country information
        country_name, country_id = _extract_country_info(hover_data, click_data)
        country_flag = get_country_flag(country_id)
        header = _create_country_header(country_flag, country_name)

        try:
            # Process data for the selected country
            total_value, category_values = _process_country_data(
                country_id, mode_data, stored_data
            )

            # Build the complete infobox with all components
            infobox_components = _build_country_infobox(
                header, country_id, category_values, total_value, selected_year
            )

            # Add inspection button for non-base map modes if country was clicked
            if map_mode != "base" and click_data:
                infobox_components.extend([_create_inspect_button()])

            _log_execution_time(start)
            return infobox_components

        except (IndexError, KeyError):
            _log_execution_time(start)
            return _create_no_data_infobox(header, country_id)

    @app.callback(
        Output(ids.CURRENT_FILTERS, "children"),
        [
            Input(ids.DONORTYPE_DROPDOWN, "value"),
            Input(ids.FLOW_TYPE_DROPDOWN, "value"),
            Input(ids.CATEGORIES_DROPDOWN, "value"),
            Input(ids.CATEGORIES_SUB_DROPDOWN, "value"),
            Input(PlaybackSliderAIO.ids.slider(ids.YEAR_SLIDER), "value"),
        ],
    )
    def update_current_filters(
        donor_types: str | list[str] | None,
        flow_types: str | list[str] | None,
        categories: str | list[str] | None,
        subcategories: str | list[str] | None,
        year: int,
    ) -> dbc.Card:
        """
        Display the currently active filters in a formatted card.

        Args:
            donor_types: Selected donor types
            flow_types: Selected flow types
            categories: Selected climate categories
            subcategories: Selected climate subcategories
            year: Selected year

        Returns:
            A Card component displaying the current filter selections
        """
        # Normalize filter values to lists
        donor_types_list = _normalize_to_list(donor_types)
        flow_types_list = _normalize_to_list(flow_types)
        categories_list = _normalize_to_list(categories)
        subcategories_list = _normalize_to_list(subcategories)

        return dbc.Card(
            [
                _create_filter_card_header(),
                _create_filter_card_body(
                    year,
                    donor_types_list,
                    flow_types_list,
                    categories_list,
                    subcategories_list,
                ),
            ],
            className="mt-0",
            style=_get_filter_card_style(),
        )


def _create_default_infobox() -> list[html.H5 | html.Div]:
    """
    Create the default infobox when no country is selected.

    Returns:
        A list of HTML components for the default infobox
    """
    header = [html.H5("🌍 Country Information ℹ️", className="infobox-header")]
    return header + [html.Div("Hover over a country for information.")]


def _extract_country_info(
    hover_data: Optional[dict], click_data: Optional[dict]
) -> Tuple[str, str]:
    """
    Extract country name and ID from hover or click data.

    Args:
        hover_data: Data from hovering over a country
        click_data: Data from clicking on a country

    Returns:
        A tuple containing the country name and ID
    """
    if click_data:
        country_name = click_data["properties"]["name"]
        country_id = click_data["id"]
    else:  # Hover data is available
        country_name = hover_data["properties"]["name"]
        country_id = hover_data["id"]

    return country_name, country_id


def _create_country_header(country_flag: str, country_name: str) -> list[html.H5]:
    """
    Create the header for a country infobox.

    Args:
        country_flag: The country's flag emoji
        country_name: The name of the country

    Returns:
        A list containing the header component
    """
    return [html.H5(f"{country_flag} {country_name}", className="infobox-header")]


def _process_country_data(
    country_id: str, mode_data: list[dict[str, Any]], stored_data: list[dict[str, Any]]
) -> Tuple[float, dict[str, float]]:
    """
    Process data for the selected country and calculate values.

    Args:
        country_id: The ISO code of the country
        mode_data: Mode-specific data
        stored_data: Climate finance data

    Returns:
        A tuple containing the total value and category values
    """
    # Calculate total value
    df_mode = pd.DataFrame(mode_data)
    df_subset = df_mode[df_mode["CountryCode"] == country_id]
    df_aggregated = aggregate(df_subset)
    total_value = round(df_aggregated["USD_Disbursement"].iloc[0], 2)

    # Extract category values
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

    category_values = {
        "adaptation": adaptation_value,
        "environment": environment_value,
        "mitigation": mitigation_value,
    }

    return total_value, category_values


def _build_country_infobox(
    header: list[html.H5],
    country_id: str,
    category_values: dict[str, float],
    total_value: float,
    selected_year: int,
) -> list[html.H5 | html.Div | html.P | html.Hr | html.Br]:
    """
    Build the complete infobox for a country with data.

    Args:
        header: The country header component
        country_id: The ISO code of the country
        category_values: dictionary of values by category
        total_value: The total disbursement value
        selected_year: The selected year

    Returns:
        A list of HTML components forming the infobox
    """
    return header + [
        html.Br(),
        html.P(f"🆔 IsoCode: {country_id}"),
        html.Hr(),
        html.P(["⚙️ Adaptation: ", html.B(f"${category_values['adaptation']} Mio USD")]),
        html.P(
            ["🌳 Environment: ", html.B(f"${category_values['environment']} Mio USD")]
        ),
        html.P(["🛡️ Mitigation: ", html.B(f"${category_values['mitigation']} Mio USD")]),
        html.Hr(),
        html.P(
            ["💰 Total Disbursements: ", html.B(f"${total_value} Mio USD")],
            className="infobox-total",
        ),
        html.P(f"📅 Year: {selected_year}"),
    ]


def _create_inspect_button() -> html.Div:
    """
    Create the button for inspecting individual flows.

    Returns:
        A Div component containing the button
    """
    return html.Div(
        [
            dbc.Button(
                "🔍 Inspect individual flows",
                id=ids.FLOW_DATA_BTN,
                n_clicks=0,
                className="inspect-btn",
            ),
        ]
    )


def _log_execution_time(start_time: float) -> None:
    """
    Log the execution time for the infobox building.

    Args:
        start_time: The start time of the operation
    """
    end = time.time()
    logger.info(f"Execution time for infobox country: {end - start_time:.2f} seconds")


def _create_no_data_infobox(
    header: list[html.H5], country_id: str
) -> list[html.H5 | html.Br | html.P]:
    """
    Create an infobox for when no data is available.

    Args:
        header: The country header component
        country_id: The ISO code of the country

    Returns:
        A list of HTML components for the no-data infobox
    """
    return header + [
        html.Br(),
        html.P(f"🆔 ID: {country_id}"),
        html.P("❌ No data available."),
    ]


def _normalize_to_list(value: str | list[str] | None) -> list[str]:
    """
    Normalize a value to a list format.

    Args:
        value: A string, list of strings, or None

    Returns:
        A list of strings, possibly empty
    """
    if isinstance(value, list):
        return value
    elif value:
        return [value]
    else:
        return []


def _create_filter_card_header() -> dbc.CardHeader:
    """
    Create the header for the filter card.

    Returns:
        A CardHeader component
    """
    return dbc.CardHeader(
        html.H6(
            "Current Filters",
            className="mb-0",
            style={
                "font-weight": "bold",
                "margin-bottom": "8px",
            },
        ),
        className="d-flex justify-content-between align-items-center",
        style={
            "background": "rgba(255, 255, 255, 0.8)",
            "border-bottom": "1px solid rgba(0, 0, 0, 0.125)",
        },
    )


def _create_filter_card_body(
    year: int,
    donor_types: list[str],
    flow_types: list[str],
    categories: list[str],
    subcategories: list[str],
) -> dbc.CardBody:
    """
    Create the body for the filter card.

    Args:
        year: The selected year
        donor_types: list of selected donor types
        flow_types: list of selected flow types
        categories: list of selected categories
        subcategories: list of selected subcategories

    Returns:
        A CardBody component with filter information
    """
    return dbc.CardBody(
        [
            html.P([html.B("Year: "), f"{year}"], className="mb-1"),
            html.P(
                [
                    html.B("Donor Type" + ("s: " if len(donor_types) > 1 else ": ")),
                    ", ".join(donor_types) if donor_types else "None",
                ],
                className="mb-1",
            ),
            html.P(
                [
                    html.B("Flow Type" + ("s: " if len(flow_types) > 1 else ": ")),
                    ", ".join(flow_types) if flow_types else "None",
                ],
                className="mb-1",
            ),
            html.P(
                [
                    html.B("Categor" + ("ies: " if len(categories) > 1 else "y: ")),
                    ", ".join(categories) if categories else "None",
                ],
                className="mb-1",
            ),
            html.P(
                [
                    html.B(
                        "Subcategor" + ("ies: " if len(subcategories) > 1 else "y: ")
                    ),
                    ", ".join(subcategories) if subcategories else "None",
                ],
                className="mb-0",
            ),
        ],
        style={"background": "rgba(255, 255, 255, 0.8)"},
    )


def _get_filter_card_style() -> dict[str, str]:
    """
    Get the CSS style for the filter card.

    Returns:
        A dictionary of CSS properties
    """
    return {
        "fontSize": "0.85rem",
        "border": "none",
        "box-shadow": "0 0 15px rgba(0, 0, 0, 0.2)",
        "border-radius": "5px",
        "color": "black",
        "width": "100%",
    }
