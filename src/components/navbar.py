import dash_bootstrap_components as dbc
from dash import Dash


def render(app: Dash):
    navbar = dbc.NavbarSimple(
        children=[
            dbc.Button(
                "Open Filters",
                id="open-offcanvas",
                n_clicks=0,
            ),
            dbc.NavItem(dbc.NavLink("Map", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("About", href="#"),
                    dbc.DropdownMenuItem("Contact", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand=app.title,
        brand_href="#",
        color="dark",
        dark=True,
    )
    return navbar
