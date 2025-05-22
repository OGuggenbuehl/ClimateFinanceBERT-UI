import dash_bootstrap_components as dbc
from dash import html

from components import ids


def render() -> html.Div:
    return html.Div(
        [
            _create_label(),
            _create_radio_items(),
        ],
    )


def _create_label() -> html.Div:
    """
    Create the label for the color mode selector.

    Returns:
        html.Div: A Div component containing the label text
    """
    return html.Div(
        "Color Distribution:",
        style={"font-weight": "bold", "margin-bottom": "4px"},
    )


def _create_radio_items() -> dbc.RadioItems:
    """
    Create the radio buttons for selecting the color mode.

    Returns:
        dbc.RadioItems: A Bootstrap RadioItems component with color mode options
    """
    return dbc.RadioItems(
        id=ids.COLOR_MODE,
        options=[
            {"label": "Continuous", "value": "continuous"},
            {"label": "Quartiles", "value": "quartile"},
        ],
        value="continuous",
        inline=True,
        className="map-control-radio",
        style={"font-size": "14px"},
    )
