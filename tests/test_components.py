"""Tests for UI components."""

import dash_bootstrap_components as dbc
from dash import html

from components import datatable, ids, navbar, welcome
from components.layout import create_layout


def test_layout_creation(app):
    """Test the creation of the main layout."""
    layout = create_layout(app)

    assert isinstance(layout, html.Div)
    assert layout.className == "app-container"

    # check if important components are present
    component_ids = [child.id for child in layout.children if hasattr(child, "id")]
    assert ids.URL in component_ids
    assert ids.STORED_DATA in component_ids
    assert ids.MODE_DATA in component_ids
    assert ids.PAGE_CONTENT in component_ids


def test_navbar_render():
    """Test the navbar rendering."""
    navbar_component = navbar.render()

    assert isinstance(navbar_component, dbc.NavbarSimple)


def test_welcome_render():
    """Test the welcome component rendering."""
    welcome_component = welcome.render()

    assert isinstance(welcome_component, dbc.Modal)
    assert welcome_component.id == ids.WELCOME_MODAL


def test_datatable_render():
    """Test the datatable rendering."""
    datatable_component = datatable.render(id="test-table")

    assert isinstance(datatable_component, html.Div)
    assert datatable_component.id == "test-table"
