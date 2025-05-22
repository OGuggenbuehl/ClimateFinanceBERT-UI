import dash_bootstrap_components as dbc
from dash import Dash, html


def render(app: Dash) -> dbc.NavbarSimple:
    """
    Render the navbar component with logo and navigation items.

    Args:
        app: The Dash application instance

    Returns:
        dbc.NavbarSimple: A Bootstrap navbar component
    """
    return dbc.NavbarSimple(
        children=_create_nav_items(),
        brand=_create_brand_with_logo(),
        brand_href="#",
        color="#0E2050",
        dark=True,
        className="py-1",  # Add padding control to navbar
        style={"max-height": "60px"},  # Set a consistent height
    )


def _create_brand_with_logo() -> html.Div:
    """
    Create the brand section with the TUM Think Tank logo.

    Returns:
        html.Div: A div containing the logo image
    """
    logo = html.Img(
        src="/assets/tumthinktank-logo-name-light.svg",  # Path to SVG file
        height="600px",  # Increased height
        className="me-2",  # Add margin to the right (Bootstrap spacing)
    )

    # Brand with logo
    return html.Div(
        [logo],
        className="d-flex align-items-center",
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
