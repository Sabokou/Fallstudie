import dash_core_components as dcc   
import dash_html_components as html 
from dash.dependencies import Input, Output 
from app import app 
from app import server 

from apps import dashboard
from apps import dashboard2
from apps import dashboard3
from apps import tool 

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Tool|', href='/apps/tool'),
        dcc.Link('Dashboard', href='/apps/dashboard'),
        dcc.Link('Dashboard2', href='/apps/dashboard2'),
        dcc.Link('Dashboard3', href='/apps/dashboard3')
    ], className="row"),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/tool':
        return tool.layout
    if pathname == '/apps/dashboard':
        return dashboard.layout
    if pathname == '/apps/dashboard2':
        return dashboard2.layout
    if pathname == '/apps/dashboard3':
        return dashboard3.layout
    else:
        return tool.layout


#if __name__ == '__main__':
app.run_server(debug=False)
    

print("hallo")