import dash_bootstrap_components as dbc
from dash import Dash, html

from components import (
    ids,
)
from components.widgets import (
    categories,
    donor_type,
    flow_type,
    sub_categories,
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
                            donor_type.render(ids.DONORTYPE_DROPDOWN),
                            html.Hr(),
                            flow_type.render(ids.FLOW_TYPE_DROPDOWN),
                            html.Hr(),
                            categories.render(ids.CATEGORIES_DROPDOWN),
                            html.Hr(),
                            sub_categories.render(ids.CATEGORIES_SUB_DROPDOWN),
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
