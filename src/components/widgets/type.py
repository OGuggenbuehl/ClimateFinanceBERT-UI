from dash import dcc, html

from components import ids


def render(id: str) -> html.Div:
    return html.Div(
        children=[
            # html.H5("Donors or Recipients?"),
            dcc.RadioItems(
                id=id,
                options=[
                    {
                        "label": html.Span(" Donors", style={"margin-right": "15px"}),
                        "value": "donors",
                    },
                    {"label": " Recipients", "value": "recipients"},
                ],
                value="donors",
                inline=True,
                className="p-2",
            ),
        ],
        className=ids.INFOBOX,
    )
