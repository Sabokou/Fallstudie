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
        dbc.Button(html.I(className="fas fa-address-card"), href="/apps/tool", color="primary", className="mr-1", block=True),
        dbc.Button(html.I(className="fas fa-chart-bar"), href="/apps/dashboard_kpi", color="primary", className="mr-1", block=True),
        dbc.Button(html.I(className="fas fa-chart-line"), href="/apps/dashboard_zeit", color="primary", className="mr-1", block=True),
        dbc.Button(html.Span([html.I(className="fas fa-plus-circle ml-2")]), href="/apps/dashboard_bcg", color="primary", className="mr-1", block=True),
    ],
    vertical=True
)

app.layout = html.Div(children = [
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col([button_group], width = 1),
        dbc.Col(html.div(className = "asset", id = 'page-content', children=[]), width = 11 )
    ])  
])

app.clientside_callback(
    """
    function(pathname) {
        if (pathname === '/apps/tool') {
            document.title = 'Verkaufstool'
        } else if (pathname === '/apps/dashboard_kpi') {
            document.title = 'Dashboard:KPI'
        } else if (pathname === '/apps/dashboard_zeit') {
            document.title = 'Dashboard:hist. Verlauf'
        } else if (pathname === '/apps/dashboard_bcg') {
            document.title = 'Dashboard:BCG'
        } else {
            document.title = 'Startseite'
        }
    }
    """,
    Output('blank-output', 'children'),
    Input('url', 'pathname')
)

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