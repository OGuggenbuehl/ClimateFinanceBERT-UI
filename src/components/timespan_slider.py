from dash import dcc, html

from components.constants import YEAR_RANGE


def render(id: str) -> html.Div:
    return html.Div(
        children=[
            html.H6("Select Timespan"),
            dcc.RangeSlider(
                id=id,
                min=YEAR_RANGE.get("min"),
                max=YEAR_RANGE.get("max"),
                step=1,
                value=[YEAR_RANGE["max"] - 2, YEAR_RANGE["max"]],
                marks={
                    str(year): str(year) if year % 5 == 0 else ""
                    for year in range(YEAR_RANGE["min"], YEAR_RANGE["max"] + 1)
                },
                allowCross=False,
            ),
        ]
    )
