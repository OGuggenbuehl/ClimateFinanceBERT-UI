import logging
import os
from typing import Any

from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from callbacks import (
    data_callbacks,
    download_callbacks,
    general_callbacks,
    info_callbacks,
    map_callbacks,
    page_callbacks,
)
from components.layout import create_layout

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_app_config() -> dict[str, Any]:
    return {
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "host": os.getenv("HOST", "127.0.0.1"),
        "port": int(os.getenv("PORT", "8050")),
    }


def create_app() -> Dash:
    app = Dash(
        __name__,
        external_stylesheets=[
            BOOTSTRAP,
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
        ],
        external_scripts=[
            "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"
        ],
        suppress_callback_exceptions=True,
    )
    app.layout = create_layout(app)
    register_callbacks(app)
    register_health_endpoint(app)

    return app


def register_callbacks(app: Dash) -> None:
    logger.info("Registering callbacks...")
    page_callbacks.register(app)
    general_callbacks.register(app)
    data_callbacks.register(app)
    info_callbacks.register(app)
    map_callbacks.register(app)
    download_callbacks.register(app)
    app.title = "ClimateFinance Explorer"
    app.layout = create_layout(app)


def register_health_endpoint(app: Dash) -> None:
    @app.server.route("/health")
    def health():
        return "OK", 200


def main():
    app = create_app()
    config = get_app_config()

    logger.info("Starting ClimateFinanceBERT UI server...")
    logger.info(f"Debug mode: {config['debug']}")
    logger.info(f"Host: {config['host']}")
    logger.info(f"Port: {config['port']}")

    app.run(
        debug=config["debug"],
        host=config["host"],
        port=config["port"],
    )


if __name__ == "__main__":
    main()
