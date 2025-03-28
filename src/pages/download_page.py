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
            dbc.Row(
                dbc.Col(
                    [
                        html.H1("Download"),
                    ],
                    width={
                        "size": 6,
                        "offset": 3,
                    },
                )
            ),
            dbc.Row(
                dbc.Col(
                    [
                        html.P(
                            "Download the data in CSV format. "
                            "You can filter the data by selecting the type of flow, "
                            "the donor type, the categories, and the subcategories."
                        ),
                    ],
                    width={
                        "size": 6,
                        "offset": 3,
                    },
                )
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        [
                            type_dropdown.render(id=ids.TYPE_DROPDOWN_DOWNLOAD),
                            donor_type_dropdown.render(
                                id="donortype-dropdown-download"
                            ),
                        ],
                        width={
                            "size": 2,
                            "offset": 1,
                        },
                    ),
                    dbc.Col(
                        [
                            year_slider.render(id=ids.YEAR_SLIDER_DOWNLOAD),
                        ],
                        width={
                            "size": 2,
                            "offset": 0,
                        },
                    ),
                    dbc.Col(
                        [
                            categories_dropdown.render(
                                id=ids.CATEGORIES_DROPDOWN_DOWNLOAD
                            ),
                            categories_sub_dropdown.render(
                                id=ids.CATEGORIES_SUB_DROPDOWN_DOWNLOAD
                            ),
                        ],
                        width={
                            "size": 2,
                            "offset": 0,
                        },
                    ),
                    dbc.Col(
                        [
                            flow_type_dropdown.render(
                                id=ids.FLOW_TYPE_DROPDOWN_DOWNLOAD
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Button(
                                            "Query",
                                            id=ids.QUERY_BTN,
                                            color="primary",
                                            className="mt-3",
                                        ),
                                        width={
                                            "size": 6,
                                            "offset": 0,
                                        },
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            "Download",
                                            id=ids.DOWNLOAD_BTN,
                                            color="primary",
                                            className="mt-3",
                                        ),
                                        width={
                                            "size": 6,
                                            "offset": 0,
                                        },
                                    ),
                                ]
                            ),
                        ],
                        width={
                            "size": 2,
                            "offset": 0,
                        },
                    ),
                ],
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        children=[
                            dbc.Card(
                                datatable.render(id=ids.DOWNLOAD_DATATABLE),
                                body=True,
                                id="download-datatable-card",
                            )
                        ],
                    ),
                    width={
                        "size": 10,
                        "offset": 1,
                    },
                )
            ),
        ],
    )
