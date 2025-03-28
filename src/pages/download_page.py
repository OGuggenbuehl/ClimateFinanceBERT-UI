import dash_bootstrap_components as dbc
from dash import Dash, html

from components import (
    categories_dropdown,
    categories_sub_dropdown,
    donor_type_dropdown,
    flow_type_dropdown,
    # map_mode,
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
                            type_dropdown.render(id="type-dropdown-download"),
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
                            year_slider.render(id="year-slider-download"),
                        ],
                        width={
                            "size": 2,
                            "offset": 0,
                        },
                    ),
                    dbc.Col(
                        [
                            categories_dropdown.render(
                                id="categories-dropdown-download"
                            ),
                            categories_sub_dropdown.render(
                                id="categories-sub-dropdown-download"
                            ),
                        ],
                        width={
                            "size": 2,
                            "offset": 0,
                        },
                    ),
                    dbc.Col(
                        [
                            # map_mode.render(top="0", bottom="0", right="0", left="0"),
                            flow_type_dropdown.render(id="flow-type-dropdown-download"),
                        ],
                        width={
                            "size": 2,
                            "offset": 0,
                        },
                    ),
                ],
            ),
        ],
    )
