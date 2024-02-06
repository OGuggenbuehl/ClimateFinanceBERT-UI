from dash import Dash, Input, Output, html

from climatefinancebert_ui.components import ids


def render(app: Dash):
    @app.callback(
        Output(ids.INFO, "children"),
        Input(ids.COUNTRIES_LAYER, "hoverData"),
    )
    def get_info(hover_data=None):
        header = [html.H5("Country Information")]
        if not hover_data:
            return header + [html.P("Hover over a country")]
        return header + [
            html.B(hover_data["properties"]["name"]),
            html.Br(),
            html.P(f"it's ID is: {hover_data['id']}"),
        ]

    # Create info control.
    info = html.Div(
        children=get_info(),
        id=ids.INFO,
        className=ids.INFO,
        style={
            "position": "absolute",
            "top": "10px",
            "right": "10px",
            "zIndex": "1000",
        },
    )
    return info
