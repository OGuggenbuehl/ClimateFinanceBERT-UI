from dash import html

from climatefinancebert_ui.components import ids


def render():
    # Return an empty Div that will be filled by the callback
    return html.Div(
        id=ids.DATATABLE,
        className=ids.DATATABLE,
    )
