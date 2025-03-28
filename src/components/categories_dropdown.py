from dash import dcc, html

from components.constants import CATEGORIES_DF


def render(id: str, style: dict = None) -> html.Div:
    return html.Div(
        children=[
            html.H6("Categories"),
            dcc.Dropdown(
                id=id,
                options=CATEGORIES_DF["climate_class"].unique(),
                value=["Mitigation"],  # CATEGORIES_DF["climate_class"].unique(),
                multi=True,
                style=style,
            ),
        ]
    )
