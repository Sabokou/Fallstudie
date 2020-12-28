#Import Dash Componenets
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
# from flask_caching import Cache

#Import Data structures
import pandas as pd
import dask.dataframe as dd
import dask.array as da
import numpy as np

#Import plotting library
import plotly.express as px

from datetime import datetime
ytd = datetime.now().year

#Programmlogik
#Einlesen der Daten
df = dd.read_sql_table("testdaten", 'sqlite:///Kundendaten.db', "Jahr")

#Daten reduzieren auf gewünschtes Jahr
df_YTD = df.loc[ytd].compute()
df_YTD.head()

#Berechnug der Werte in den "Werte-Karten"
Gewinn_YTD = df_YTD["Gewinn"].sum()
Anzahl_YTD = df_YTD["Anzahl"].sum()

#Websiten-Aufbau
layout = html.Div([
    html.H1(children="KPI´s im Zeitverlauf"),
    dcc.Tabs(id="tabs_kpi", value='Gewinn', children=[
        dcc.Tab(label='Gewinn', value='Gewinn'),
        dcc.Tab(label='Anzahl', value='Anzahl'),
    ]),

    html.H2("Erfolg der Produkte"),
    html.Div(id="Produktplot_1"),

    html.H2("KPI´s im Zeitverlauf"),
    html.Div(id="Wert_Karte",children =[
        html.H3("Werte im aktuellen Jahr"),
        dcc.Markdown(f'''Gewinn     {Gewinn_YTD}'''),
        dcc.Markdown(f'''Anzahl     {Anzahl_YTD}''')
        ]),


    html.H2("Features im Zeitverlauf"),
    dcc.RadioItems(
    id="radio_kpi",
    options=[
        {'label': 'Geschlecht', 'value': 'Geschlecht'},
        {'label': 'Altersklassen', 'value': 'Alter'},
        {'label': 'Beruf', 'value': 'Job'},
        {'label': 'Familienstand', 'value': 'Familienstand'},
        {'label': 'Kinder', 'value': 'Kinder'},
        {'label': 'Gehaltsklasse', 'value': 'Gehalt'}
    ],
    value='Geschlecht',
    labelStyle={'display': 'inline-block'}
    ), 
    html.Div(id="Produktplot_2")
])

@app.callback(Output(component_id = "Produktplot_1", component_property= 'children'),
              Input(component_id = 'tabs_kpi', component_property= 'value'))
def render_content(tab):
    return html.Div([
        dcc.Graph(figure=fetch_figure_bar(fetch_dataframe_sum(df_YTD, tab, ["Angebotenes Produkt"]),\
        "Angebotenes Produkt", tab,  title = tab + " verkaufter Produkter [YTD]" ))
        ])

    
@app.callback(Output("Produktplot_2", 'children'),
              Input('tabs_kpi', 'value'),
              Input("radio_kpi", 'value'))
def render_content(tab, radio):
    temp_df = fetch_dataframe_sum(df_YTD, tab, ["Angebotenes Produkt", radio])
    temp_fig = fetch_figure_bar(temp_df, radio, tab,\
             color = "Angebotenes Produkt",  title = tab + " verkaufter Produkte nach " + radio + " [YTD]" )
    
    return html.Div([
            dcc.Graph(figure=temp_fig)
    ])

def fetch_figure_line(dataframe, x, y, title, color = None, text = None):
    #frame = fetch_dataframe(dataframe, groupDirection, args)
    if color != None and text == None:
        return px.line(dataframe, x=x, y=y, color=color, title=title)
    elif color == None and text == None:
        return px.line(dataframe, x=x, y=y, title=title)
    elif color == None and text != None:
         return px.line(dataframe, x=x, y=y, title=title, text=text)
    else:
        return px.line(dataframe, x=x, y=y, title=title, color=color, text=text)
    
def fetch_figure_bar(dataframe, x, y, title, color = None, text = None):
    if color != None and text == None:
        return px.bar(dataframe, x=x, y=y, color=color, title=title)
    elif color == None and text == None:
        return px.bar(dataframe, x=x, y=y, title=title)
    elif color == None and text != None:
        fig_temp = px.bar(dataframe, x=x, y=y, title=title, text=text)
        fig_temp.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig_temp.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        return fig_temp
    else:
        fig_temp = px.bar(dataframe, x=x, y=y, title=title, color=color, text=text)
        fig_temp.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig_temp.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        return fig_temp

def fetch_dataframe_sum(dataframe, groupDirection, args):
    #return dataframe.groupby(args).sum().reset_index().compute()
    return dataframe.groupby(args).sum().reset_index()
# def fetch_dataframe_count(dataframe, groupDirection, args):
#     return dataframe.groupby(args).count().reset_index()
