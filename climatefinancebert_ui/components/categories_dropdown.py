from dash import Dash, dcc, html

from climatefinancebert_ui.components import ids


def render(app: Dash) -> html.Div:
    categories = [
        "mitigation",
        "adaption",
        "environment",
        "climate_finance",
        # "climate_finance_+_environment",
    ]

    return html.Div(
        children=[
            html.H6("Categories"),
            dcc.Dropdown(
                id=ids.CATEGORIES_DROPDOWN,
                options=[
                    {
                        "label": category.replace("_", " ").title(),
                        "value": category.replace("_", " ").title(),
                    }
                    for category in categories
                ],
                value=[category.replace("_", " ").title() for category in categories],
                multi=True,
            ),
        ]
    )
