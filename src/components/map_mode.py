import dash_bootstrap_components as dbc
from dash import html

import components.ids as ids


def render(top: str, bottom: str, right: str, left: str):
    return html.Div(
        [
            html.H5("Choose a map mode 🎛️"),
            dbc.RadioItems(
                # TODO: add linebreak for options due to length and overlap
                options=[
                    {"label": "Base", "value": "base"},
                    # {"label": "Total Flows", "value": "total"}, ## removed 'total' mode for now
                    {
                        "label": "OECD Rio Markers",
                        "value": "rio_oecd",
                        "disabled": False,
                    },
                    {
                        "label": "ClimateFinanceBERT Predictions",
                        "value": "rio_climfinbert",
                        "disabled": False,
                    },
                    {"label": "Difference", "value": "rio_diff", "disabled": False},
                ],
                value="base",
                id=ids.MAP_MODE,
                inline=True,
            ),
        ],
        style={
            # "position": "absolute",
            "top": top,
            "bottom": bottom,
            "right": right,
            "left": left,
        },
        className=ids.INFOBOX,
    )
