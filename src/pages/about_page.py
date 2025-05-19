import dash_bootstrap_components as dbc
from dash import Dash, html


def render(app: Dash) -> html.Div:
    return html.Div(
        id="about-page",
        className="container mt-4",
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1("About", className="mb-4 text-center"),
                            html.P(
                                "This dashboard provides an interactive overview of bilateral climate finance flows across countries, categories, and over time. As part of a research project by ETH Zurich and the University of St.Gallen a machine-learning model was trained to identify climate relevance and different categories in development assistance funding in a consistent and replicable way. The goal of the project is to improve transparency and accuracy in international climate finance reporting.",
                                className="mb-4",
                            ),
                            html.H3("Data Source"),
                            html.P(
                                "The underlying data are drawn from the OECD Creditor Reporting System (CRS), which contains textual descriptions and project-level information on Official Development Assistance (ODA) reported by contributing countries.",
                                className="mb-4",
                            ),
                            html.H3("Methodology"),
                            html.P(
                                "Climate finance flows are estimated using ClimateFinanceBERT, a transformer-based machine learning model developed to classify climate-relevant development assistance projects. The model was trained on a manually annotated dataset and achieves over 95% accuracy in identifying and categorizing projects as contributing to either mitigation, adaptation, or the environment and respective subcategories. The classification approach focuses on projects with a principal climate objective, in line with Rio marker guidelines, to produce conservative but consistent estimates.",
                                className="mb-4",
                            ),
                            html.H3("Publication"),
                            html.P(
                                [
                                    "The methodology and findings are detailed in the following peer-reviewed article:",
                                    html.Br(),
                                    "Toetzke, M., Stünzi, A., & Egli, F. (2022). Consistent and replicable estimation of bilateral climate finance. ",
                                    html.A(
                                        "Nature Climate Change, 12, 897–900.",
                                        href="https://doi.org/10.1038/s41558-022-01482-7",
                                        target="_blank",
                                    ),
                                ],
                                className="mb-4",
                            ),
                            html.H3("Code and Data"),
                            html.P(
                                [
                                    "The full codebase and training data for the ClimateFinanceBERT model are ",
                                    html.A(
                                        "openly available on GitHub",
                                        href="https://github.com/MalteToetzke/consistent-and-replicable-estimation-of-bilateral-climate-finance",
                                        target="_blank",
                                    ),
                                ],
                                className="mb-4",
                            ),
                            html.H3("Affiliation"),
                            html.P(
                                [
                                    "The development of this dashboard was supported by the ",
                                    html.A(
                                        "Transformation Finance Lab (TFL)",
                                        href="https://tumthinktank.de/de/projekt/transformation-finance-lab/",
                                        target="_blank",
                                    ),
                                    "The Transformation Finance Lab brings together tomorrow's leaders in the finance industry to create a community of practice, shape policy and build tools that mobilize finance for the sustainability transformation, leveraging TUM’s expertise in data analysis and visualization. The TFL is part of the TUM Think Tank, a university-based platform that fosters collaboration between academia, civil society, business, and the public sector to shape a responsible, human-centered digital future.",
                                ],
                            ),
                        ],
                        width={"size": 10, "offset": 1},
                        lg={"size": 8, "offset": 2},
                    )
                ]
            )
        ],
    )
