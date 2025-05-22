import dash_bootstrap_components as dbc
from dash import Dash


def render(app: Dash) -> dbc.NavbarSimple:
    return dbc.NavbarSimple(
        children=_create_nav_items(),
        brand=app.title,
        brand_href="#",
        color="dark",
        dark=True,
    )


def _create_nav_items() -> list[dbc.NavItem]:
    """
    Create the navigation items for the navbar.

    Returns:
        List[dbc.NavItem]: A list of navigation items
    """
    return [
        dbc.NavItem(dbc.NavLink("Map 🗺️", href="/")),
        dbc.NavItem(dbc.NavLink("Download 📥", href="/download")),
        dbc.NavItem(dbc.NavLink("About 🔬", href="/about")),
    ]
