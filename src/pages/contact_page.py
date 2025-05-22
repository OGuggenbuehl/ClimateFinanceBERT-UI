import dash_bootstrap_components as dbc
from dash import html


def render() -> html.Div:
    return html.Div(
        id="contact-page",
        children=[_create_contact_column()],
    )


def _create_contact_column() -> dbc.Col:
    """
    Create the main content column with contact information.

    Returns:
        dbc.Col: A Bootstrap column with contact details
    """
    return dbc.Col(
        [
            _create_title(),
            _create_contact_info(),
        ],
        width={"size": 6, "offset": 3},
    )


def _create_title() -> html.H1:
    """
    Create the page title.

    Returns:
        html.H1: The title component
    """
    return html.H1("Contact")


def _create_contact_info() -> html.P:
    """
    Create the contact information text.

    Returns:
        html.P: A paragraph with contact information
    """
    return html.P("Find us on GitHub")
