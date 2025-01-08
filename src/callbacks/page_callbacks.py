from components import ids
from dash import Input, Output, html
from pages import about_page, contact_page, map_page


def register(app):
    @app.callback(Output(ids.PAGE_CONTENT, "children"), Input(ids.URL, "pathname"))
    def display_page(pathname):
        if pathname == "/":
            return map_page.render(app)
        elif pathname == "/about":
            return about_page.render(app)
        elif pathname == "/contact":
            return contact_page.render(app)
        else:
            return html.Div(
                [
                    html.H1("404: Not found", className="text-danger"),
                    html.Hr(),
                    html.P(f"The pathname {pathname} was not recognized..."),
                ]
            )
