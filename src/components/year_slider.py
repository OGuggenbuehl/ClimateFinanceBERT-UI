from dash import html

from components import ids
from components.slider_player import PlaybackSliderAIO


def render() -> html.Div:
    min = 2010
    max = 2022
    return html.Div(
        children=[
            html.H6("Select Year"),
            PlaybackSliderAIO(
                aio_id=ids.YEAR_SLIDER,
                slider_props={"min": min, "max": max, "step": 1, "value": 2020},
                button_props={"className": "float-left"},
            ),
        ]
    )
