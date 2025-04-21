import dash_bootstrap_components as dbc
import ids
from dash import html


def render(app):
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle(f"Welcome to {app.title}! 👋")),
            dbc.ModalBody(
                [
                    html.H5(
                        "Interactive Climate Finance Explorer",
                        className="text-center mb-3",
                    ),
                    html.P(
                        "This dashboard allows you to explore climate finance flows between countries "
                        "using data classified by ClimateFinanceBERT, a natural language processing model "
                        "specialized in climate finance."
                    ),
                    html.Hr(),
                    html.H6("Getting Started:"),
                    html.Ul(
                        [
                            html.Li(
                                "Use the map to visualize finance flows between countries"
                            ),
                            html.Li(
                                "Filter data by donor type, flow type, categories, and subcategories"
                            ),
                            html.Li("Click on countries to see detailed information"),
                            html.Li(
                                "Use the time slider to explore data over different years"
                            ),
                            html.Li(
                                "Download data for further analysis from the Download tab"
                            ),
                        ]
                    ),
                    html.P(
                        "For more information about the project, visit the About section.",
                        className="text-muted mt-3",
                    ),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Get Started",
                    id=ids.WELCOME_MODAL_CLOSE,
                    className="ms-auto",
                )
            ),
        ],
        id=ids.WELCOME_MODAL,
        is_open=True,
        size="lg",
        centered=True,
    )
