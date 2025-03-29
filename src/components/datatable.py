from dash import html

from components import ids


def render(id: str):
    # Return an empty Div that will be filled by the callback
    return html.Div(
        id=id,
        className=ids.DATATABLE,
    )
