from dash import Input, Output, html

from components import ids
from pages import about_page, download_page, map_page


def register(app):
    @app.callback(
        Output(ids.PAGE_CONTENT, "children"),
        Input(ids.URL, "pathname"),
    )
    def display_page(pathname):
        if pathname == "/":
            return map_page.render()
        elif pathname == "/about":
            return about_page.render()
        elif pathname == "/download":
            return download_page.render()
        else:
            return html.Div(
                [
                    html.H1("404: Not found", className="text-danger"),
                    html.Hr(),
                    html.P(f"The pathname {pathname} was not recognized..."),
                ]
            )
