from components import ids
from dash import html


def render():
    # Return an empty Div that will be filled by the callback
    return html.Div(
        id=ids.DATATABLE,
        className=ids.DATATABLE,
    )
