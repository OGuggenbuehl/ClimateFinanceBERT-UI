from dash import html

from components.constants import YEAR_RANGE
from components.slider_player import PlaybackSliderAIO


def render(id: str) -> html.Div:
    return html.Div(
        children=[
            html.H6("Select Year"),
            PlaybackSliderAIO(
                aio_id=id,
                slider_props={
                    "min": YEAR_RANGE["min"],
                    "max": YEAR_RANGE["max"],
                    "step": 1,
                    "value": 2020,
                },
                button_props={"className": "float-left"},
            ),
        ]
    )
