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

button_group = dbc.ButtonGroup(
    [
        dbc.Button("Verkaufstool", href="/apps/tool", color="primary", className="mr-1", block=True),
        dbc.Button("Dashboard KPI", href="/apps/dashboard_kpi", color="primary", className="mr-1", block=True),
        dbc.Button("Dashboard Zeit", href="/apps/dashboard_zeit", color="primary", className="mr-1", block=True),
        dbc.Button("Dashboard BCG", href="/apps/dashboard_bcg", color="primary", className="mr-1", block=True),
    ],
    vertical=True
)

app.layout = html.Div(children = [
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col([button_group], width = 1),
        dbc.Col(html.Div(className = "asset", id = 'page-content', children=[]), width = 11 )
    ])  
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