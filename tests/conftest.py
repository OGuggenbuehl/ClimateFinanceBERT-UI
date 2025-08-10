"""Common test fixtures for ClimateFinanceBERT-UI."""

import os
import sys

import pandas as pd
import pytest
from dash.testing.application_runners import ThreadedRunner
from dash.testing.composite import DashComposite

# add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


@pytest.fixture
def app():
    """Create a Dash app instance for testing."""
    from app import create_app

    app = create_app()
    return app


@pytest.fixture
def dash_duo():
    """Create a DashComposite for UI testing."""
    with DashComposite(ThreadedRunner()) as dc:
        yield dc


@pytest.fixture
def sample_finance_data():
    """Create a sample DataFrame for testing data operations."""
    return pd.DataFrame(
        {
            "DEDonorcode": ["USA", "DEU", "GBR", "FRA", "JPN"],
            "DonorName": [
                "United States",
                "Germany",
                "United Kingdom",
                "France",
                "Japan",
            ],
            "DERecipientcode": ["IND", "BRA", "ZAF", "IDN", "MEX"],
            "RecipientName": ["India", "Brazil", "South Africa", "Indonesia", "Mexico"],
            "Year": [2020, 2020, 2021, 2021, 2022],
            "FlowType": ["Grant", "Loan", "Equity", "Grant", "Loan"],
            "DonorType": [
                "Bilateral",
                "Multilateral",
                "Bilateral",
                "Multilateral",
                "Bilateral",
            ],
            "Category": [
                "Mitigation",
                "Adaptation",
                "Mitigation",
                "Adaptation",
                "Cross-cutting",
            ],
            "ClimateRelevance": [1.0, 0.8, 0.5, 0.7, 0.9],
            "USDTotal": [1000000, 2000000, 1500000, 2500000, 3000000],
            "USDMitigationAmount": [1000000, 0, 1500000, 0, 1500000],
            "USDAdaptationAmount": [0, 2000000, 0, 2500000, 1500000],
        }
    )


@pytest.fixture
def mock_duckdb_conn(monkeypatch):
    """Mock the DuckDB connection."""

    class MockConnection:
        def execute(self, query):
            # return a mock cursor
            return MockCursor()

        def close(self):
            pass

    class MockCursor:
        def fetchdf(self):
            # return a sample DataFrame
            return pd.DataFrame(
                {
                    "DEDonorcode": ["USA", "DEU"],
                    "DonorName": ["United States", "Germany"],
                    "DERecipientcode": ["IND", "BRA"],
                    "RecipientName": ["India", "Brazil"],
                    "Year": [2020, 2020],
                    "USDTotal": [1000000, 2000000],
                }
            )

    import duckdb

    monkeypatch.setattr(duckdb, "connect", lambda *args, **kwargs: MockConnection())
    return MockConnection()
