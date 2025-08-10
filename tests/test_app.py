"""Tests for app creation."""

import os

from dash import Dash


def test_create_app(monkeypatch):
    """Test app creation."""

    # Arrange
    # Use a more flexible mock that can handle both 1 and 2 arguments
    def mock_getenv(key, default=None):
        return default

    monkeypatch.setattr(os, "getenv", mock_getenv)

    # Act
    from app import create_app, get_app_config

    app = create_app()
    config = get_app_config()

    # Assert
    assert isinstance(app, Dash)
    assert app.title == "ClimateFinance Explorer"
    assert "debug" in config
    assert "host" in config
    assert "port" in config
    assert config["host"] == "127.0.0.1"
    assert config["port"] == 8050


def test_app_config_with_env_vars(monkeypatch):
    """Test app configuration with environment variables."""
    # Arrange
    env_vars = {
        "DEBUG": "true",
        "HOST": "0.0.0.0",
        "PORT": "5000",
    }
    monkeypatch.setattr(os, "getenv", lambda key, default: env_vars.get(key, default))

    # Act
    from app import get_app_config

    config = get_app_config()

    # Assert
    assert config["debug"] is True
    assert config["host"] == "0.0.0.0"
    assert config["port"] == 5000
