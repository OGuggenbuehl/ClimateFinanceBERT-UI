from components import ids
from dash import Input, Output, State


def register(app):
    @app.callback(
        Output("offcanvas", "is_open"),
        Input(ids.OPEN_FILTERS, "n_clicks"),
        [State("offcanvas", "is_open")],
    )
    def toggle_sidebar(n1, is_open):
        """Toggle the sidebar when the button is clicked."""
        if n1:
            return not is_open
        return is_open

    @app.callback(
        Output(ids.COUNTRIES_LAYER, "clickData"),
        [Input(ids.RESET_MAP, "n_clicks")],
    )
    def reset_clickData(n_clicks):
        return None
