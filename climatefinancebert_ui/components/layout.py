import dash_bootstrap_components as dbc
from dash import Dash, html

from climatefinancebert_ui.components import map, year_dropdown


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
                dbc.Col(
                    html.Div(
                        className="dropdown-container",
                        children=[
                            year_dropdown.render(app),
                        ],
                    ),
                    width=3,
                )
            ),
        ],
    )
