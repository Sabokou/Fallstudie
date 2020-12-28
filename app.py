#python version 3.8.3 64-bit
#imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#import for caching
# import os
# from flask_caching import Cache

app = dash.Dash(__name__, suppress_callback_exceptions=True, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}])

server = app.server 

# cache = Cache(app.server, config={
#     'CACHE_TYPE': 'filesystem',
# })

