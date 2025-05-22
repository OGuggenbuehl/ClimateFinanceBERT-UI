import dash_bootstrap_components as dbc
from dash import html


def render() -> dbc.NavbarSimple:
    return dbc.NavbarSimple(
        children=_create_nav_items(),
        brand=_create_brand_with_logo(),
        brand_href=None,  # Remove the default brand href to allow logo link to work
        color="#0E2050",
        dark=True,
        className="py-1",
        style={"height": "56px"},
    )


def _create_brand_with_logo() -> html.Div:
    """
    Create the brand section with the TUM Think Tank logo.

    Returns:
        html.Div: A div containing the logo image with a link
    """
    logo = html.Img(
        src="/assets/tumthinktank-logo-name-light.svg",
        className="me-2",
    )

    return html.Div(
        [
            html.A(
                logo,
                href="https://tumthinktank.de/de/projekt/transformation-finance-lab/",
                target="_blank",  # Opens in a new tab
            )
        ],
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
