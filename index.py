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

app.layout = html.Div(className="wrapper", children = [
    dcc.Location(id='url', refresh=False),
    html.Div(className="menüleiste", children=[
        dcc.Link('Tool', className = "menü", href ='/apps/tool'),
        dcc.Link('KPIs', className = "menü", href ='/apps/dashboard_kpi'),
        dcc.Link('Zeitverlauf', className = "menü", href ='/apps/dashboard_zeit'),
        dcc.Link('BCG-Matrix', className = "menü", href ='/apps/dashboard_bcg')
    ]),    
    html.Div(className = "asset", id = 'page-content', children=[]),
    
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
        return tool.layout


#if __name__ == '__main__':
app.run_server(debug=True)

print("Server terminated")