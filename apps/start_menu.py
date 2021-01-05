#Import Dash Componenets
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div(children=[
    dbc.Row([
        dbc.Col(html.Div(children = [
            html.Img(src = "/assets/Logo.png", style = {"max-width":"55%", "height":"auto"}),
            html.H2("Dashboard für Verkaufsentwicklungen und Produktberatung")
        ]), width=4)
    ],justify="center", align="center", className="h-50"),
])