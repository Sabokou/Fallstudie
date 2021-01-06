#Import Dash Componenets
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

layout = html.Div(children=[
    dbc.Row([
        dbc.Col(
            html.Div(children = [
                html.Img(src = "/assets/Logo.png", style = {"max-width":"50%", "height":"auto"})
            ]), width={"size": 6, "offset": 3}
        )
    ], justify="center",),
    dbc.Row([
        html.Div(children = [
            html.H2("Dashboard für Produktverkaufsentwicklungen und Produktberatung")
        ])
    ], justify="center",)
], style =CONTENT_STYLE)