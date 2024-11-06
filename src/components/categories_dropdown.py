from components import ids
from components.constants import CATEGORIES_DF
from dash import Dash, dcc, html


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
