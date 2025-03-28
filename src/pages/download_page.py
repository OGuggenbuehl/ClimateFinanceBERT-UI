import dash_bootstrap_components as dbc
from dash import Dash, html

from components import (
    categories_dropdown,
    categories_sub_dropdown,
    datatable,
    donor_type_dropdown,
    flow_type_dropdown,
    ids,
    type_dropdown,
    year_slider,
)


def render(app: Dash) -> html.Div:
    return html.Div(
        id="download-page",
        children=[
            # Title
            dbc.Row(
                dbc.Col(
                    [
                        html.H1("Download Data", className="text-center my-4"),
                    ],
                    width=12,
                )
            ),
            # Description Text
            dbc.Row(
                dbc.Col(
                    [
                        html.P(
                            "Download the data in CSV format. You can filter the data "
                            "by selecting the type of flow, the donor type, the categories, "
                            "and the subcategories. Once you're ready, click 'Query' to pull the data and 'Download' to get it in CSV format.",
                            className="lead text-center",
                        ),
                    ],
                    width=12,
                )
            ),
            html.Br(),
            # Filter Controls - Grid Layout
            dbc.Row(
                children=[
                    # Left Filters (Type & Donor Type)
                    dbc.Col(
                        [
                            type_dropdown.render(id=ids.TYPE_DROPDOWN_DOWNLOAD),
                            donor_type_dropdown.render(
                                id="donortype-dropdown-download"
                            ),
                        ],
                        width={
                            "size": 2,
                            "offset": 2,
                        },
                        className="mb-4",
                    ),
                    # Middle Filter (Year Slider)
                    dbc.Col(
                        [
                            year_slider.render(id=ids.YEAR_SLIDER_DOWNLOAD),
                        ],
                        width={
                            "size": 4,
                            "offset": 0,
                        },
                        className="mb-4",
                    ),
                    # Right Filters (Categories & Flow Type)
                    dbc.Col(
                        [
                            categories_dropdown.render(
                                id=ids.CATEGORIES_DROPDOWN_DOWNLOAD
                            ),
                            categories_sub_dropdown.render(
                                id=ids.CATEGORIES_SUB_DROPDOWN_DOWNLOAD
                            ),
                            flow_type_dropdown.render(
                                id=ids.FLOW_TYPE_DROPDOWN_DOWNLOAD
                            ),
                        ],
                        width={
                            "size": 2,
                            "offset": 0,
                        },
                        className="mb-4",
                    ),
                ],
                className="mb-4",  # Add margin at the bottom
            ),
            # Query & Download Buttons in One Row
            dbc.Row(
                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button(
                                    "Query",
                                    id=ids.QUERY_BTN,
                                    color="primary",
                                    className="w-100",
                                ),
                                width={
                                    "size": 2,
                                    "offset": 4,
                                },
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Download",
                                    id=ids.DOWNLOAD_BTN,
                                    color="success",
                                    className="w-100",
                                ),
                                width=2,
                            ),
                        ],
                        className="g-3",  # Grid gap between buttons
                    ),
                    width=12,
                ),
                className="mb-4",  # Add margin at the bottom
            ),
            # Data Table Display
            dbc.Row(
                dbc.Col(
                    html.Div(
                        children=[
                            dbc.Card(
                                datatable.render(id=ids.DOWNLOAD_DATATABLE),
                                body=False,
                                id=ids.DATATABLE_CARD_DOWNLOAD,
                                className="shadow-sm",
                            )
                        ],
                    ),
                    width={
                        "size": 8,
                        "offset": 2,
                    },
                ),
                className="mt-4",  # Margin on top of the datatable card
            ),
        ],
    )
