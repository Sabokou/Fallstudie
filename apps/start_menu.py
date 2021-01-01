#Import Dash Componenets
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div(children=[
    dbc.Row([
        html.Div(children = [
            html.Img(src = "")
        ])
    ]),
    dbc.Row([
        html.Div(children = [
            html.H2("Dashboard für Produktverkaufsentwicklungen und Produktberatung")
        ])
    ]),
    dbc.Row([
        html.Div(children = [])
    ])
])