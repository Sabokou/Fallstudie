import dash_core_components as dcc   
import dash_html_components as html 
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output 

from app import app 
from app import server 

from apps import dashboard_kpi
from apps import dashboard_zeit
from apps import dashboard_bcg
from apps import tool 
from apps import start_menu

app.layout = html.Div(children = [
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col([
            dbc.Row([html.Div(children=[dcc.Link('Tool', href ='/apps/tool')])]),
            dbc.Row([html.Div(children=[dcc.Link('KPIs', href ='/apps/dashboard_kpi')])]),
            dbc.Row([html.Div(children=[dcc.Link('Zeit', href ='/apps/dashboard_zeit')])]),
            dbc.Row([html.Div(children=[dcc.Link('BCG', href ='/apps/dashboard_bcg')])])
        ], width = 2)
    ]),
        dbc.Col(html.Div(className = "asset", id = 'page-content', children=[]), width = 10 )
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/tool':
        return tool.layout
    if pathname == '/apps/dashboard_kpi':
        return dashboard_kpi.layout
    if pathname == '/apps/dashboard_zeit':
        return dashboard_zeit.layout
    if pathname == '/apps/dashboard_bcg':
        return dashboard_bcg.layout
    else:
        return start_menu.layout


#if __name__ == '__main__':
app.run_server(debug=True)

print("Server terminated")