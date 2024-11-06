from components import ids
from dash import Dash, dcc, html


def render(app: Dash) -> html.Div:
    min = 2000
    max = 2020
    return html.Div(
        children=[
            html.H6("Years"),
            dcc.RangeSlider(
                id=ids.YEAR_SLIDER,
                min=min,
                max=max,
                step=1,
                value=[min, max],
                marks={
                    str(year): str(year) if year % 5 == 0 else "" for year in range(min, max + 1)
                },
                allowCross=False,
            ),
        ]
    )
