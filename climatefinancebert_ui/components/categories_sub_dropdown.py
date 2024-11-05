from dash import Dash, dcc, html

from climatefinancebert_ui.components import ids
from climatefinancebert_ui.components.constants import CATEGORIES_DF


def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            html.H6("Subcategories"),
            dcc.Dropdown(
                id=ids.CATEGORIES_SUB_DROPDOWN,
                options=CATEGORIES_DF["meta_category"].unique(),
                value=None,
                multi=True,
            ),
        ]
    )
