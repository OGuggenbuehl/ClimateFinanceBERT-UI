from dash import dcc, html

DONOR_TYPE_MAP = {
    "bilateral": "Donor Country",
    "multilateral": "Multilateral Donor",
    "private": "Private Donor",
}


def render(id: str) -> html.Div:
    return html.Div(
        children=[
            html.H6("Donor Type"),
            dcc.Dropdown(
                id=id,
                options=[
                    {"label": type.title(), "value": DONOR_TYPE_MAP[type]}
                    for type in DONOR_TYPE_MAP
                ],
                value=DONOR_TYPE_MAP["bilateral"],
                multi=True,
            ),
        ]
    )
