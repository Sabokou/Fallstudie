#Import Dash Componenets
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import datetime as dt

#Import Plotting Libarary
import plotly.express as px

#Import data backend
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('sqlite:///Kundendaten.db', execution_options={"sqlite_raw_colnames": True})
df = pd.read_sql("allgemeine_daten", con = engine)

#Programmlogik
# currentYear = dt.datetime.now().year
# df_jahr = df.where("Jahr" == str(currentYear))

#Websiten-Aufbau
layout = html.Div([




])