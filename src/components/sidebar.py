import dash_bootstrap_components as dbc
from dash import Dash, html

from components import (
    categories_dropdown,
    categories_sub_dropdown,
    donor_type_dropdown,
    type_dropdown,
    year_slider,
)


def render(app: Dash):
    offcanvas = html.Div(
        [
            dbc.Offcanvas(
                [
                    html.P("Mix and match your selection to filter the data"),
                    dbc.Nav(
                        [
                            type_dropdown.render(),
                            html.Br(),
                            donor_type_dropdown.render(),
                            html.Br(),
                            categories_dropdown.render(),
                            html.Br(),
                            categories_sub_dropdown.render(),
                            html.Br(),
                            year_slider.render(),
                        ],
                        vertical=True,
                        pills=True,
                    ),
                ],
                id="offcanvas",
                title="Filters",
                is_open=False,
            ),
        ]
    )

    return offcanvas
