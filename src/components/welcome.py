import dash_bootstrap_components as dbc
from dash import html

from components import ids


def render():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Welcome to ClimateFinanceBERT UI! 👋")),
            dbc.ModalBody(
                [
                    html.Div(
                        [
                            html.H4(
                                "Interactive Climate Finance Explorer",
                                className="text-center mb-3 text-muted",
                            ),
                            html.P(
                                "This dashboard allows you to explore climate finance flows between countries "
                                "using data classified by ClimateFinanceBERT, a large language model "
                                "specialized in climate finance.",
                                className="lead text-center px-4 text-muted",
                            ),
                        ],
                        className="bg-light p-3 rounded mb-4",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H4(
                                        ["Getting Started:"],
                                        className="mb-3",
                                    ),
                                    html.Ul(
                                        [
                                            html.Li(
                                                [
                                                    "🗺️ Use the map to visualize finance flows between countries"
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Li(
                                                [
                                                    "🔍 Filter data by donor type, flow type, categories, and subcategories"
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Li(
                                                [
                                                    "👆 Click on countries to see detailed information"
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Li(
                                                [
                                                    "🎚️ Use the time slider to explore data over different years"
                                                ],
                                                className="mb-2",
                                            ),
                                            html.Li(
                                                [
                                                    "📥 Download data for further analysis from the Download tab"
                                                ],
                                                className="mb-2",
                                            ),
                                        ],
                                        className="list-unstyled",
                                    ),
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                [
                                    html.H4(
                                        ["Default Filters:"],
                                        className="mb-3",
                                    ),
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.Ul(
                                                        [
                                                            html.Li(
                                                                [
                                                                    "🏛️ Donor Type: ",
                                                                    html.Span(
                                                                        "Bilateral",
                                                                        className="fw-bold",
                                                                    ),
                                                                ],
                                                                className="mb-2",
                                                            ),
                                                            html.Li(
                                                                [
                                                                    "↔️ Flow Type: ",
                                                                    html.Span(
                                                                        "ODA Grants",
                                                                        className="fw-bold",
                                                                    ),
                                                                ],
                                                                className="mb-2",
                                                            ),
                                                            html.Li(
                                                                [
                                                                    "🏷️ Categories: ",
                                                                    html.Span(
                                                                        "Mitigation",
                                                                        className="fw-bold",
                                                                    ),
                                                                ],
                                                                className="mb-2",
                                                            ),
                                                            html.Li(
                                                                [
                                                                    "☀️ Sub-categories: ",
                                                                    html.Span(
                                                                        "Solar Energy",
                                                                        className="fw-bold",
                                                                    ),
                                                                ],
                                                                className="mb-2",
                                                            ),
                                                        ],
                                                        className="list-unstyled",
                                                    ),
                                                ]
                                            )
                                        ],
                                        className="shadow-sm",
                                    ),
                                ],
                                width=6,
                            ),
                        ],
                        className="px-3",
                    ),
                    dbc.Alert(
                        [
                            "⚠️ ",
                            html.Strong("Performance Note: "),
                            html.P(
                                "The application's performance may suffer if too many categories are selected simultaneously. "
                                "For optimal experience, consider limiting your selection. "
                                "When downloading data, the filters are set separately in the download tab.",
                                className="mb-0 ms-4",
                            ),
                        ],
                        color="warning",
                        className="mt-4 mb-3",
                    ),
                    html.P(
                        [
                            "ℹ️ For more information about the project, visit the About section.",
                        ],
                        className="text-muted mt-2 fst-italic text-center",
                    ),
                ]
            ),
        ],
        id=ids.WELCOME_MODAL,
        is_open=True,
        size="lg",
        centered=True,
        backdrop=True,
        className="welcome-modal",
    )
