import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html

from climatefinancebert_ui.components import datatable, ids, map, navbar, sidebar, utils


def create_layout(app: Dash) -> html.Div:
    # Callback to load selected dataset into a shared store
    @app.callback(
        Output("stored-data", "data"),
        [Input(ids.TYPE_DROPDOWN, "value")],
    )
    def update_stored_data(selected_type):
        df_full = utils.fetch_data(selected_type)
        return df_full.to_dict("records")

    return html.Div(
        className="app-container",
        children=[
            navbar.render(app),
            dcc.Store(id="stored-data"),  # The store to keep the selected dataset
            dbc.Container(
                fluid=True,  # Set the container to be fluid
                children=[
                    dbc.Col(
                        [
                            sidebar.render(app),
                            dbc.Row(
                                dbc.Col(
                                    html.Div(
                                        className="map-container",
                                        children=[
                                            dbc.Card(
                                                map.render(app),
                                                body=True,
                                                className="map-card",
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
                                            dbc.Card(
                                                datatable.render(app),
                                                body=True,
                                            )
                                        ],
                                    ),
                                    width=12,
                                )
                            ),
                        ],
                        width={
                            "size": 12,
                            "offset": 0,
                        },
                    ),
                ],
            ),
        ],
    )
