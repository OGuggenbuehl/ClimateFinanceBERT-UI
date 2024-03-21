from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from climatefinancebert_ui.callbacks import (
    data_callbacks,
    general_callbacks,
    info_callbacks,
)
from climatefinancebert_ui.components.layout import create_layout


def main():
    app = Dash(external_stylesheets=[BOOTSTRAP])
    general_callbacks.register(app)
    data_callbacks.register(app)
    info_callbacks.register(app)
    app.title = "ClimateFinanceBERT UI"
    app.layout = create_layout(app)
    app.run_server(debug=True, host="0.0.0.0", port=9000)


if __name__ == "__main__":
    main()
