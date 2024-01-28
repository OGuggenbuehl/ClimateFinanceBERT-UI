from dash import Dash, Input, Output, html


def render(app: Dash):
    @app.callback(
        Output("click-info", "children"),
        [
            Input("countries", "clickData"),
        ],
    )
    def display_click_data(click_data):
        if click_data is not None:
            # Process click data here
            return f"You clicked {click_data['properties']['name']}"
        else:
            return "Click on a country"

    return html.Div(children=html.Plaintext(id="click-info"))
