import uuid
from typing import Any, Optional

import dash_bootstrap_components as dbc
from dash import MATCH, Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from components.constants import YEAR_RANGE


def create_year_markers(min_year: int, max_year: int, step: int = 1) -> dict[int, str]:
    """Create year markers for the slider with labels every 5 years.

    Args:
        min_year: Minimum year value
        max_year: Maximum year value
        step: Step size between years

    Returns:
        Dictionary mapping year values to marker labels
    """
    return {
        year: (str(year) if year % 5 == 0 else "")
        for year in range(min_year, max_year + 1, step)
    }


def create_slider_props(props: dict[str, Any]) -> dict[str, Any]:
    """Create slider properties with appropriate markers and tooltip.

    Args:
        props: Base slider properties

    Returns:
        Enhanced slider properties
    """
    min_year = props.get("min", 2000)
    max_year = props.get("max", 2020)
    step = props.get("step", 1)

    # Create slider marks
    marks = create_year_markers(min_year, max_year, step)

    # Add marks and tooltip to props
    props["marks"] = marks
    props["tooltip"] = {
        "placement": "bottom",
        "always_visible": True,
    }  # keeps the selected value visible

    return props


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
    """All-in-one component for year selection with playback animation.

    This component combines a slider for year selection with play/pause
    controls for animating through years.
    """

    class ids:
        """Component IDs for the PlaybackSliderAIO elements."""

        @staticmethod
        def play(aio_id):
            """ID for the play/pause button."""
            return {
                "component": "PlaybackSliderAIO",
                "subcomponent": "button",
                "aio_id": aio_id,
            }

        @staticmethod
        def play_icon(aio_id):
            """ID for the play/pause button icon."""
            return {
                "component": "PlaybackSliderAIO",
                "subcomponent": "i",
                "aio_id": aio_id,
            }

        @staticmethod
        def slider(aio_id):
            """ID for the year slider."""
            return {
                "component": "PlaybackSliderAIO",
                "subcomponent": "slider",
                "aio_id": aio_id,
            }

        @staticmethod
        def interval(aio_id):
            """ID for the interval component controlling animation speed."""
            return {
                "component": "PlaybackSliderAIO",
                "subcomponent": "interval",
                "aio_id": aio_id,
            }

    # Make ids accessible as a class attribute
    ids = ids

    def __init__(
        self,
        aio_id: Optional[str] = None,
        button_props: Optional[dict[str, Any]] = None,
        slider_props: Optional[dict[str, Any]] = None,
        interval_props: Optional[dict[str, Any]] = None,
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # Initialize property dictionaries
        button_props = button_props.copy() if button_props else {}
        slider_props = slider_props.copy() if slider_props else {}
        interval_props = interval_props.copy() if interval_props else {}

        # Set button to inactive initially
        button_props["active"] = False

        # Create enhanced slider properties
        slider_props = create_slider_props(slider_props)

        # Create component layout
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

        # Increment value by step, loop back to min if we reach max
        new_val = value + step
        if new_val > max:
            new_val = min

        return new_val
