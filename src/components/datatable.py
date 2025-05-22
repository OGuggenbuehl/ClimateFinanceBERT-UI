from dash import html

from components import ids


def render(id: str) -> html.Div:
    return html.Div(
        id=id,
        className=ids.DATATABLE,
    )
