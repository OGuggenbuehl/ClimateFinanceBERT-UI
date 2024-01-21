import dash_leaflet as dl
import polars as pl
from components.layout import create_layout
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP


def main() -> None:
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "ClimateFinanceBERT-UI"
    app.layout = create_layout(app)
    app.run()


if __name__ == "__main__":
    main()
