import dash_bootstrap_components as dbc
from dash import Dash, html


def render(app: Dash):
    logo = html.Img(
        src="/assets/tumthinktank-logo-name-light.svg",  # Path to your SVG file
        height="600px",  # Increased height
        className="me-2",  # Add margin to the right (Bootstrap spacing)
    )

    # Brand with logo
    brand = html.Div(
        [
            logo,
            # app.title,
        ],
        className="d-flex align-items-center",
    )

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Map 🗺️", href="/")),
            dbc.NavItem(dbc.NavLink("Download 📥", href="/download")),
            dbc.NavItem(dbc.NavLink("About 🔬", href="/about")),
        ],
        brand=brand,  # Use our custom brand component
        brand_href="#",
        color="#0E2050",
        dark=True,
        className="py-1",  # Add padding control to navbar
        style={"max-height": "60px"},  # Set a consistent height
    )
    return navbar
