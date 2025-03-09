from components import ids
from dash import Dash, dcc, html


def render(app: Dash) -> html.Div:
    donor_types = {
        "bilateral": "Donor Country",
        "multilateral": "Multilateral Donor",
    }

    return html.Div(
        children=[
            html.H6("Donor Type"),
            dcc.Dropdown(
                id=ids.DONORTYPE_DROPDOWN,
                options=[
                    {"label": type.title(), "value": donor_types[type]}
                    for type in donor_types
                ],
                value=donor_types["bilateral"],
                multi=True,
            ),
        ]
    )
