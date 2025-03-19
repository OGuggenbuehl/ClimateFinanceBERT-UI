from dash import html

from components import ids


def render():
    # Return an empty Div that will be filled by the callback
    return html.Div(
        id=ids.FLOW_DATA_TABLE,
        className=ids.DATATABLE,
    )
