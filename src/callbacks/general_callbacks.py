from dash import Input, Output, State

from components import ids


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

    @app.callback(
        Output(ids.FLOW_DATA_MODAL, "is_open"),
        [
            Input(ids.FLOW_DATA_BTN, "n_clicks"),
        ],
        [State(ids.FLOW_DATA_MODAL, "is_open")],
        prevent_initial_call=True,
    )
    def toggle_modal(
        btn_clicked,
        is_open,
    ):
        if btn_clicked:
            return not is_open
        return is_open
