import dash_bootstrap_components as dbc
from dash import Dash, html

from components import datatable, ids
from components.widgets import (
    action_button,
    categories,
    donor_type,
    flow_type,
    sub_categories,
    timespan,
)


def render(app: Dash) -> html.Div:
    return html.Div(
        id="download-page",
        children=[
            # title
            dbc.Row(
                dbc.Col(
                    [
                        html.H1("Download Data", className="text-center my-4"),
                    ],
                    width=12,
                )
            ),
            # description
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
            # filters row
            dbc.Row(
                children=[
                    # left column
                    dbc.Col(
                        [
                            donor_type.render(
                                id=ids.DONORTYPE_DROPDOWN_DOWNLOAD,
                                style={
                                    "color": "black",
                                },
                            ),
                            flow_type.render(
                                id=ids.FLOW_TYPE_DROPDOWN_DOWNLOAD,
                                style={
                                    "color": "black",
                                },
                            ),
                        ],
                        width={
                            "size": 2,
                            "offset": 2,
                        },
                        className="mb-4",
                    ),
                    # middle column
                    dbc.Col(
                        [
                            timespan.render(id=ids.YEAR_SLIDER_DOWNLOAD),
                        ],
                        width={
                            "size": 4,
                            "offset": 0,
                        },
                        className="mb-4",
                    ),
                    # right column
                    dbc.Col(
                        [
                            categories.render(
                                id=ids.CATEGORIES_DROPDOWN_DOWNLOAD,
                                style={
                                    "color": "black",
                                },
                            ),
                            sub_categories.render(
                                id=ids.CATEGORIES_SUB_DROPDOWN_DOWNLOAD,
                                style={
                                    "color": "black",
                                },
                            ),
                        ],
                        width={
                            "size": 2,
                            "offset": 0,
                        },
                        className="mb-4",
                    ),
                ],
                className="mb-4",
            ),
            dbc.Row(
                dbc.Col(
                    # buttons row
                    dbc.Row(
                        [
                            dbc.Col(
                                action_button.render(
                                    "Query",
                                    id=ids.QUERY_BTN,
                                    class_name="w-100",
                                ),
                                width={
                                    "size": 2,
                                    "offset": 4,
                                },
                            ),
                            dbc.Col(
                                action_button.render(
                                    "Download",
                                    id=ids.DOWNLOAD_BTN,
                                    color="success",
                                    class_name="w-100",
                                ),
                                width=2,
                            ),
                        ],
                        className="g-3",
                    ),
                    width=12,
                ),
                className="mb-4",
            ),
            # html.Br(),
            # datatable row
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
                className="mt-4",
            ),
        ],
    )
