from dash import Dash, dcc, html

from climatefinancebert_ui.components import ids


def render(app: Dash) -> html.Div:
    all_years = range(2000, 2020)

    return html.Div(
        children=[
            html.H6("Year"),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=[{"label": year, "value": year} for year in all_years],
                value=1,
                multi=False,
            ),
        ]
    )
