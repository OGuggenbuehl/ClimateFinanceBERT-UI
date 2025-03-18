from dash import Dash, dcc, html

from components import ids
from components.constants import CATEGORIES_DF


def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            html.H6("Subcategories"),
            dcc.Dropdown(
                id=ids.CATEGORIES_SUB_DROPDOWN,
                options=CATEGORIES_DF["meta_category"].unique(),
                value=["Solar-energy"],  # CATEGORIES_DF["meta_category"].unique(),
                multi=True,
            ),
        ]
    )
