import dash_bootstrap_components as dbc
from dash import Dash, html

from climatefinancebert_ui.components import (
    categories_dropdown,
    datatable,
    map,
    type_dropdown,
    year_slider,
)


def create_layout(app: Dash) -> html.Div:
    return dbc.Container(
        className="app-div",
        children=[
            dbc.Row(
                dbc.Col(
                    html.H1(app.title),
                )
            ),
            html.Hr(),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        className="map-container",
                        children=[
                            map.render(
                                app,
                            )
                        ],
                    )
                )
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            className="dropdown-container",
                            children=[
                                year_slider.render(app),
                            ],
                        ),
                        width=5,
                    ),
                    dbc.Col(
                        html.Div(
                            className="dropdown-container",
                            children=[
                                type_dropdown.render(app),
                            ],
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        html.Div(
                            className="dropdown-container",
                            children=[
                                categories_dropdown.render(app),
                            ],
                        ),
                        width=5,
                    ),
                ]
            ),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        className="datatable-container",
                        children=[
                            datatable.render(app),
                        ],
                    ),
                    width=12,
                )
            ),
        ],
    )
