import os

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
    app = Dash(
        __name__,
        external_stylesheets=[BOOTSTRAP],
        suppress_callback_exceptions=True,
    )
    page_callbacks.register(app)
    general_callbacks.register(app)
    data_callbacks.register(app)
    info_callbacks.register(app)
    map_callbacks.register(app)
    app.title = "ClimateFinanceBERT UI"
    app.layout = create_layout(app)
    app.run_server(
        debug=True,
        host=os.getenv("DOCKER_HOST", "127.0.0.1"),
        port=os.getenv("DOCKER_PORT", "8050"),
    )


if __name__ == "__main__":
    main()
