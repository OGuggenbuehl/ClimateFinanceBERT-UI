from components import ids
from components.slider_player import PlaybackSliderAIO
from dash import Dash, html


def render(app: Dash) -> html.Div:
    min = 2010
    max = 2022
    return html.Div(
        children=[
            html.H6("Years"),
            # dcc.RangeSlider(
            #     id=ids.YEAR_SLIDER,
            #     min=min,
            #     max=max,
            #     step=1,
            #     value=[2020, 2021],
            #     marks={
            #         str(year): str(year) if year % 5 == 0 else ""
            #         for year in range(min, max + 1)
            #     },
            #     allowCross=False,
            # ),
            PlaybackSliderAIO(
                aio_id=ids.YEAR_SLIDER,
                slider_props={"min": min, "max": max, "step": 1, "value": 2020},
                button_props={"className": "float-left"},
            ),
        ]
    )
