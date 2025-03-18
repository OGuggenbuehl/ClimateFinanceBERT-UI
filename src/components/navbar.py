import dash_bootstrap_components as dbc
from dash import Dash


def render(app: Dash):
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Map 🗺️", href="/")),
            dbc.NavItem(dbc.NavLink("About 🔬", href="/about")),
        ],
        brand=app.title,
        brand_href="#",
        color="dark",
        dark=True,
    )
    return navbar
