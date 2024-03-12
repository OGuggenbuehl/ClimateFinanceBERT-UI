import pandas as pd
from dash import Dash, Input, Output, dash_table, html

from climatefinancebert_ui.components import ids


def render(app: Dash):
    # Return an empty Div that will be filled by the callback
    return html.Div(
        id=ids.DATATABLE,
        className=ids.DATATABLE,
    )
