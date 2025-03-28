from dash import dcc, html


def render(id: str) -> html.Div:
    types = ["donors", "recipients"]

    return html.Div(
        children=[
            html.H6("Donors or Recipients?"),
            dcc.Dropdown(
                id=id,
                options=[{"label": type.title(), "value": type} for type in types],
                value="donors",
                multi=False,
            ),
        ]
    )
