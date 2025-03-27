import dash_bootstrap_components as dbc
from dash import Dash, html

from components import (
    categories_dropdown,
    categories_sub_dropdown,
    donor_type_dropdown,
    flow_type_dropdown,
    type_dropdown,
)


def render(app: Dash):
    offcanvas = html.Div(
        [
            dbc.Offcanvas(
                [
                    html.P("Mix and match your selection to filter the data"),
                    dbc.Nav(
                        [
                            html.Hr(),
                            type_dropdown.render(),
                            html.Hr(),
                            donor_type_dropdown.render(),
                            html.Hr(),
                            flow_type_dropdown.render(),
                            html.Hr(),
                            categories_dropdown.render(),
                            html.Hr(),
                            categories_sub_dropdown.render(),
                        ],
                        vertical=True,
                        pills=True,
                    ),
                ],
                id="offcanvas",
                title=html.B("Filters"),
                is_open=False,
            ),
        ]
    )

    return offcanvas
