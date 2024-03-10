import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, html

from climatefinancebert_ui.components import (
    categories_dropdown,
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
                            type_dropdown.render(app),
                            html.Br(),
                            categories_dropdown.render(app),
                            html.Br(),
                            year_slider.render(app),
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

    @app.callback(
        Output("offcanvas", "is_open"),
        Input("open-offcanvas", "n_clicks"),
        [State("offcanvas", "is_open")],
    )
    def toggle_sidebar(n1, is_open):
        if n1:
            return not is_open
        return is_open

    return offcanvas
