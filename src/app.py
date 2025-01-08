from callbacks import (
    data_callbacks,
    general_callbacks,
    info_callbacks,
    map_callbacks,
    page_callbacks,
)
from components.layout import create_layout
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP


def main():
    app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
    page_callbacks.register(app)
    general_callbacks.register(app)
    data_callbacks.register(app)
    info_callbacks.register(app)
    map_callbacks.register(app)
    app.title = "ClimateFinanceBERT UI"
    app.layout = create_layout(app)
    app.run_server(debug=True, host="0.0.0.0", port=9000)


if __name__ == "__main__":
    main()
