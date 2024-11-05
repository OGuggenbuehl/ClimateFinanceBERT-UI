from dash import Dash, dcc, html

from climatefinancebert_ui.components import ids
from climatefinancebert_ui.components.constants import CATEGORIES_DF


def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            html.H6("Categories"),
            dcc.Dropdown(
                id=ids.CATEGORIES_DROPDOWN,
                options=CATEGORIES_DF["climate_class"].unique(),
                value=CATEGORIES_DF["climate_class"].unique(),
                multi=True,
            ),
        ]
    )
