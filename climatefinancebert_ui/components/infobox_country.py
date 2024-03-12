from dash import Dash, Input, Output, html

from climatefinancebert_ui.components import ids


def render(
    app: Dash,
    top: str,
    bottom: str,
    right: str,
    left: str,
):
    @app.callback(
        Output(ids.INFOBOX_COUNTRY, "children"),
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
        id=ids.INFOBOX_COUNTRY,
        className=ids.INFOBOX,
        style={
            "position": "absolute",
            "top": top,
            "bottom": bottom,
            "right": right,
            "left": left,
            "zIndex": "1000",
        },
    )
