#Import Dash Componenets
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div(children=[
    dbc.Row([
        html.Div(children = [
            #TODO: find way to get a relative path to image
            html.Img(src = "/assets/Logo_Plutos.svg")
        ])
    ], justify="center",),
    dbc.Row([
        html.Div(children = [
            html.H2("Dashboard für Produktverkaufsentwicklungen und Produktberatung")
        ])
    ], justify="center",)
])