import dash_bootstrap_components as dbc
from dash import Dash, html

from climatefinancebert_ui.components import (
    categories_dropdown,
    datatable,
    map,
    type_dropdown,
    year_slider,
)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


def build_sidebar(app: Dash) -> html.Div:
    return html.Div(
        [
            html.H3("Filters"),
            html.Hr(),
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
        style=SIDEBAR_STYLE,
    )


def create_layout(app: Dash) -> html.Div:
    return dbc.Container(
        className="app-div",
        children=[
            dbc.Col(
                build_sidebar(app),
                width=3,
            ),
            dbc.Col(
                [
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
                            ),
                            width=12,
                        )
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
                width={"size": 9, "offset": 3},
            ),
        ],
    )
