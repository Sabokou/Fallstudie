#python version 3.8.3 64-bit
#imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

#import for caching
import os
from flask_caching import Cache

font_awesome = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"

app = dash.Dash(__name__, suppress_callback_exceptions=True,\
      meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],\

      external_stylesheets=[dbc.themes.BOOTSTRAP, font_awesome],\
      title= "Dashboard",
      update_title='Berechne...')

app.title = 'Plutos Consulting'

server = app.server 

cache = Cache(server, config={
     'CACHE_TYPE': 'simple'})

