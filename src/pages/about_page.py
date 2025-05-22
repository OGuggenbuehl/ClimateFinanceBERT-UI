import dash_bootstrap_components as dbc
from dash import html


def render() -> html.Div:
    return html.Div(
        id="about-page",
        className="container mt-4 mb-4",
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            _create_header(),
                            _create_subtitle(),
                            _create_intro_section(),
                            _create_info_cards_row(),
                            _create_publication_card(),
                            _create_code_data_card(),
                            _create_affiliation_card(),
                        ],
                        width={"size": 12},
                        lg={"size": 10, "offset": 1},
                    )
                ]
            )
        ],
    )


def _create_header() -> html.H1:
    """
    Create the page header.

    Returns:
        html.H1: The page title component
    """
    return html.H1(
        "About ClimateFinanceBERT",
        className="mb-4 text-center fw-bold",
    )


def _create_subtitle() -> html.H4:
    """
    Create the page subtitle.

    Returns:
        html.H4: The subtitle component
    """
    return html.H4(
        "The Natural Language Model underlying ClimateFinance Explorer",
        className="mb-4 text-center",
    )


def _create_intro_section() -> html.Div:
    """
    Create the introduction section with project overview.

    Returns:
        html.Div: The introduction component
    """
    return html.Div(
        className="bg-light p-4 rounded-3 shadow-sm mb-5",
        children=[
            html.P(
                "This application provides an interactive overview of bilateral climate finance flows across countries, categories, and over time. As part of a research project by ETH Zurich and the University of St.Gallen a machine-learning model was trained to identify climate relevance and different categories in development assistance funding in a consistent and replicable way. The goal of the project is to improve transparency and accuracy in international climate finance reporting.",
                className="lead mb-0 text-dark",  # Added text-dark class to ensure visibility
            ),
        ],
    )


def _create_info_cards_row() -> dbc.Row:
    """
    Create the row with data source and methodology information cards.

    Returns:
        dbc.Row: A Bootstrap row with two information cards
    """
    return dbc.Row(
        [
            _create_data_source_column(),
            _create_methodology_column(),
        ],
        className="mb-4",
    )


def _create_data_source_column() -> dbc.Col:
    """
    Create the column with data source information.

    Returns:
        dbc.Col: A Bootstrap column with the data source card
    """
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardHeader(
                    html.H3(
                        [
                            "🌎 ",
                            html.Span("Data Source"),
                        ],
                        className="h5 mb-0",
                    )
                ),
                dbc.CardBody(
                    html.P(
                        "The underlying data are drawn from the OECD Creditor Reporting System (CRS), which contains textual descriptions and project-level information on Official Development Assistance (ODA) reported by contributing countries.",
                        className="mb-0",
                    )
                ),
            ],
            className="h-100 shadow-sm",
        ),
        md=6,
        className="mb-4",
    )


def _create_methodology_column() -> dbc.Col:
    """
    Create the column with methodology information.

    Returns:
        dbc.Col: A Bootstrap column with the methodology card
    """
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardHeader(
                    html.H3(
                        [
                            "🧠 ",
                            html.Span("Methodology"),
                        ],
                        className="h5 mb-0",
                    )
                ),
                dbc.CardBody(
                    html.P(
                        "Climate finance flows are estimated using ClimateFinanceBERT, a transformer-based machine learning model developed to classify climate-relevant development assistance projects. The model was trained on a manually annotated dataset and achieves over 95% accuracy in identifying and categorizing projects as contributing to either mitigation, adaptation, or the environment and respective subcategories.",
                        className="mb-0",
                    )
                ),
            ],
            className="h-100 shadow-sm",
        ),
        md=6,
        className="mb-4",
    )


def _create_publication_card() -> dbc.Card:
    """
    Create the card with publication information.

    Returns:
        dbc.Card: A Bootstrap card with publication details
    """
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H3(
                    ["📑 ", html.Span("Publication")],
                    className="h5 mb-0",
                )
            ),
            dbc.CardBody(
                [
                    html.P(
                        "The methodology and findings are detailed in the following peer-reviewed article:",
                        className="mb-3",
                    ),
                    dbc.Alert(
                        [
                            html.Strong("Toetzke, M., Stünzi, A., & Egli, F. (2022). "),
                            "Consistent and replicable estimation of bilateral climate finance. ",
                            html.A(
                                "Nature Climate Change, 12, 897–900.",
                                href="https://doi.org/10.1038/s41558-022-01482-7",
                                target="_blank",
                                className="alert-link",
                            ),
                        ],
                        color="info",
                        className="mb-0",
                    ),
                ]
            ),
        ],
        className="mb-4 shadow-sm",
    )


def _create_code_data_card() -> dbc.Card:
    """
    Create the card with code and data information.

    Returns:
        dbc.Card: A Bootstrap card with code repository details
    """
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H3(
                    ["💻 ", html.Span("Code and Data")],
                    className="h5 mb-0",
                )
            ),
            dbc.CardBody(
                [
                    html.P(
                        [
                            "The full codebase and training data for the ClimateFinanceBERT model are ",
                            html.A(
                                "openly available on GitHub",
                                href="https://github.com/MalteToetzke/consistent-and-replicable-estimation-of-bilateral-climate-finance",
                                target="_blank",
                                className="fw-bold",
                            ),
                        ],
                        className="mb-0",
                    ),
                ]
            ),
        ],
        className="mb-4 shadow-sm",
    )


def _create_affiliation_card() -> dbc.Card:
    """
    Create the card with affiliation information.

    Returns:
        dbc.Card: A Bootstrap card with affiliation details
    """
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H3(
                    ["🏢 ", html.Span("Affiliation")],
                    className="h5 mb-0",
                )
            ),
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.P(
                                [
                                    "The development of this dashboard was supported by the ",
                                    html.A(
                                        "Transformation Finance Lab (TFL)",
                                        href="https://tumthinktank.de/de/projekt/transformation-finance-lab/",
                                        target="_blank",
                                        className="fw-bold",
                                    ),
                                ],
                                className="mb-2",
                            ),
                            html.P(
                                "The Transformation Finance Lab brings together tomorrow's leaders in the finance industry to create a community of practice, shape policy and build tools that mobilize finance for the sustainability transformation, leveraging TUM's expertise in data analysis and visualization.",
                                className="mb-2",
                            ),
                            html.P(
                                "The TFL is part of the TUM Think Tank, a university-based platform that fosters collaboration between academia, civil society, business, and the public sector to shape a responsible, human-centered digital future.",
                                className="mb-0",
                            ),
                        ]
                    ),
                ]
            ),
        ],
        className="shadow-sm",
    )
