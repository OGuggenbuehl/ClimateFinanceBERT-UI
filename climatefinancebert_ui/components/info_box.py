from dash import Dash, Input, Output, html

from climatefinancebert_ui.components import ids


def render(app: Dash):
    @app.callback(
        Output(ids.INFO, "children"),
        Input(ids.COUNTRIES_LAYER, "hoverData"),
    )
    def build_infobox(hover_data=None):
        header = [html.H5("Country Information")]
        if not hover_data:
            return header + [html.P("Hover over a country")]
        return header + [
            html.B(hover_data["properties"]["name"]),
            html.Br(),
            html.P(f"it's ID is: {hover_data['id']}"),
        ]

    return html.Div(
        children=build_infobox(),
        id=ids.INFO,
        className=ids.INFO,
        style={
            "position": "absolute",
            "top": "20px",
            "right": "100px",
            "zIndex": "1000",
        },
    )
