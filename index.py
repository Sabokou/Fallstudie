import dash_core_components as dcc   
import dash_html_components as html 
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output 

from app import app 
from app import server
from app import dash

#from apps import dashboard_kpi
#from apps import dashboard_zeit
#from apps import dashboard_bcg
from apps import tool 
from apps import start_menu





app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("JungBank", className="display-4"),
        html.Hr(),
        html.P(
            "Wählen Sie die gewünschte Anwendung", className="lead"
        ),
        
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Tool", href="/apps/tool", active="exact"),
                dbc.NavLink("dashboard_kpi", href="/apps/dashboard_kpi", active="exact"),
                dbc.NavLink("dashboard_zeit", href="/apps/dashboard_zeit", active="exact"),
                dbc.NavLink("dashboard_bcg", href="/apps/dashboard_bcg", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

#content = html.Div(id="page-content", style=CONTENT_STYLE)

#app.layout = html.Div([dcc.Location(id="url"), sidebar, content])





app.layout = html.Div(children = [
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col([sidebar], width = 1),
        dbc.Col(html.Div(className = "asset", id = 'page-content', children=[]), width = 11 )
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