from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from climatefinancebert_ui.components.layout import create_layout


def main():
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "ClimateFinanceBERT UI"
    app.layout = create_layout(app)
    app.run()


if __name__ == "__main__":
    main()
