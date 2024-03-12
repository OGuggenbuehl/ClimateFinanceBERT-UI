from dash import Input, Output, State


def register(app):
    @app.callback(
        Output("offcanvas", "is_open"),
        Input("open-offcanvas", "n_clicks"),
        [State("offcanvas", "is_open")],
    )
    def toggle_sidebar(n1, is_open):
        # TODO: Add docstring
        if n1:
            return not is_open
        return is_open
