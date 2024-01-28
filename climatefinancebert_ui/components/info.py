from dash import Dash, Input, Output, html

from climatefinancebert_ui.components import ids

test_url = (
    "https://raw.githubusercontent.com/MalteToetzke/"
    "consistent-and-replicable-estimation-of-bilateral-climate-finance/"
    "main/Data/Recipients/recipients_2016.csv"
)


def render(app: Dash):
    @app.callback(
        Output(ids.INFO_BOX, "children"),
        Input(ids.COUNTRIES_LAYER, "clickData"),
    )
    def display_click_data(click_data):
        if click_data is not None:
            # Process click data here
            return f"You clicked {click_data['properties']['name']}"
        else:
            return "Click on a country"

    return html.Div(children=html.Plaintext(id=ids.INFO_BOX))
