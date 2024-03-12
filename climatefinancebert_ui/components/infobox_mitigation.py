from dash import Dash, Input, Output, html

from climatefinancebert_ui.components import ids


def render(
    app: Dash,
):
    @app.callback(
        Output(ids.INFOBOX_MITIGATION, "children"),
        Input(ids.YEAR_SLIDER, "value"),
    )
    def build_infobox(year=None):
        header = [html.H5("Mitigation Information")]
        if not year:
            return header + [html.P("Select a year")]
        return header + [
            html.P(f"Showing data from {year[0]} - {year[1]}"),
        ]

    return html.Div(
        children=build_infobox(),
        id=ids.INFOBOX_MITIGATION,
        className=ids.INFOBOX,
        style={
            # "position": "absolute",
            "zIndex": "1000",
        },
    )
