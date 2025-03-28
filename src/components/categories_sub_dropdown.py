from dash import dcc, html

from components.constants import CATEGORIES_DF


def render(id: str) -> html.Div:
    return html.Div(
        children=[
            html.H6("Subcategories"),
            dcc.Dropdown(
                id=id,
                options=CATEGORIES_DF["meta_category"].unique(),
                value=["Solar-energy"],  # CATEGORIES_DF["meta_category"].unique(),
                multi=True,
            ),
        ]
    )
