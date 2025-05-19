import uuid

import dash_bootstrap_components as dbc
from dash import MATCH, Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from components.constants import YEAR_RANGE


def render(id: str) -> html.Div:
    return html.Div(
        children=[
            html.H6(
                "Select Year",
                style={
                    "font-weight": "bold",
                    "margin-bottom": "8px",
                },
            ),
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


class PlaybackSliderAIO(html.Div):
    class ids:
        def play(aio_id):
            return {
                "component": "PlaybackSliderAIO",
                "subcomponent": "button",
                "aio_id": aio_id,
            }

        def play_icon(aio_id):
            return {
                "component": "PlaybackSliderAIO",
                "subcomponent": "i",
                "aio_id": aio_id,
            }

        def slider(aio_id):
            return {
                "component": "PlaybackSliderAIO",
                "subcomponent": "slider",
                "aio_id": aio_id,
            }

        def interval(aio_id):
            return {
                "component": "PlaybackSliderAIO",
                "subcomponent": "interval",
                "aio_id": aio_id,
            }

    ids = ids

    def __init__(
        self,
        aio_id=None,
        button_props=None,
        slider_props=None,
        interval_props=None,
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        button_props = button_props.copy() if button_props else {}
        slider_props = slider_props.copy() if slider_props else {}
        interval_props = interval_props.copy() if interval_props else {}

        button_props["active"] = False

        min_year = slider_props.get("min", 2000)
        max_year = slider_props.get("max", 2020)
        step = slider_props.get("step", 1)

        # ticks yearly but only label every 5 years
        marks = {
            year: (str(year) if year % 5 == 0 else "")
            for year in range(min_year, max_year + 1, step)
        }

        slider_props["marks"] = marks
        slider_props["tooltip"] = {
            "placement": "bottom",
            "always_visible": True,
        }  # keeps the selected value visible

        super().__init__(
            [
                dbc.Button(
                    html.I(id=self.ids.play_icon(aio_id)),
                    id=self.ids.play(aio_id),
                    **button_props,
                ),
                dcc.Slider(id=self.ids.slider(aio_id), **slider_props),
                dcc.Interval(id=self.ids.interval(aio_id), **interval_props),
            ]
        )

    @callback(
        Output(ids.play(MATCH), "active"),
        Output(ids.play_icon(MATCH), "className"),
        Output(ids.interval(MATCH), "disabled"),
        Input(ids.play(MATCH), "n_clicks"),
        State(ids.play(MATCH), "active"),
    )
    def toggle_play(clicks, curr_status):
        if clicks:
            text = "fa-solid fa-play" if curr_status else "fa-solid fa-pause"
            return not curr_status, text, curr_status
        return curr_status, "fa-solid fa-play", not curr_status

    @callback(
        Output(ids.slider(MATCH), "value"),
        Input(ids.play(MATCH), "active"),
        Input(ids.interval(MATCH), "n_intervals"),
        State(ids.slider(MATCH), "min"),
        State(ids.slider(MATCH), "max"),
        State(ids.slider(MATCH), "step"),
        State(ids.slider(MATCH), "value"),
    )
    def start_playback(play, interval, min, max, step, value):
        if not play:
            raise PreventUpdate

        new_val = value + step
        if new_val > max:
            new_val = min

        return new_val
