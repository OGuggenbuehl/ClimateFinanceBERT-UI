import dash_bootstrap_components as dbc
from dash import html

import components.ids as ids


def render(top: str, bottom: str, right: str, left: str) -> html.Div:
    return html.Div(
        [
            _create_heading(),
            _create_radio_items(),
        ],
        style=_get_container_style(top, bottom, right, left),
        className=ids.INFOBOX,
    )


def _create_heading() -> html.H5:
    """
    Create the heading for the map mode selector.

    Returns:
        html.H5: A heading element with the title text
    """
    return html.H5("Choose a map mode 🎛️")


def _create_radio_items() -> dbc.RadioItems:
    """
    Create the radio buttons for selecting the map mode.

    Returns:
        dbc.RadioItems: A Bootstrap RadioItems component with map mode options
    """
    return dbc.RadioItems(
        # TODO: add linebreak for options due to length and overlap
        options=_get_map_mode_options(),
        value="rio_climfinbert",
        id=ids.MAP_MODE,
        inline=True,
    )


def _get_map_mode_options() -> list[dict]:
    """
    Get the list of map mode options.

    Returns:
        list[dict]: A list of option dictionaries for the RadioItems component
    """
    return [
        {"label": "Base", "value": "base"},
        # {"label": "Total Flows", "value": "total"}, ## removed 'total' mode for now
        # {
        #     "label": "OECD Rio Markers",
        #     "value": "rio_oecd",
        #     "disabled": False,
        # },
        {
            "label": "ClimateFinanceBERT Predictions",
            "value": "rio_climfinbert",
            "disabled": False,
        },
        # {"label": "Difference", "value": "rio_diff", "disabled": False},
    ]


def _get_container_style(top: str, bottom: str, right: str, left: str) -> dict:
    """
    Get the CSS style for the container div.

    Args:
        top: CSS top position value
        bottom: CSS bottom position value
        right: CSS right position value
        left: CSS left position value

    Returns:
        dict: A dictionary with the CSS style properties
    """
    return {
        # "position": "absolute",
        "top": top,
        "bottom": bottom,
        "right": right,
        "left": left,
        "display": "none",  # hide map-modes for now without breaking functionality
    }
