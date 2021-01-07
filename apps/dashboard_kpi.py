#Import Dash Componenets
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from flask_caching import Cache

#Import notwendige Komponenten der App
from app import app
from app import cache

#Import Data structures
import pandas as pd
import dask.dataframe as dd
import dask.array as da
import numpy as np

#Import plotting library
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime
ytd = datetime.now().year

#Programmlogik
@cache.memoize()
def fetch_dataframe(ytd):
    #Einlesen der Daten
    df = dd.read_sql_table("testdaten", 'sqlite:///Kundendaten.db', "Jahr")

    #Daten reduzieren auf gewünschtes Jahr
    try:
        df_YTD = df.loc[ytd].compute()
    except:
        df_YTD = df.loc[ytd-1].compute()
        print(f"Keine Daten in Jahr {ytd} vorhanden. Lade Vorjahresdaten...")
    return df_YTD

#region KPI Indikatoren erzeugen
@cache.memoize()
def fetch_kpi_indicator(Gewinn_YTD, Anzahl_YTD, Prob_YTD):
    fig = go.Figure()

    fig.update_layout(height = 300)

    fig.add_trace(go.Indicator(
        mode = "number",
        value = Gewinn_YTD,
        title = {"text": "Gewinn"},
        number = {'suffix': "€"},
        domain = {'x': [0, 0.5], 'y': [0.6, 1]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = Anzahl_YTD,
        title = {"text": "Anzahl"},
        number = {'suffix':" "},
        domain = {'x': [0.6, 1], 'y': [0.6, 1]}))

    fig.add_trace(go.Indicator(
        mode = "number",
        value = Prob_YTD,
        title = {"text": "Kaufwahrscheinlichkeit"},
        number = {'suffix': "%"},
        domain = {'x': [0.3, 0.7], 'y': [0, 0.4]}))

    return fig
#endregion

#region Mapping für Graphen-Gruppierungen
def Altersklassen(A):
    if A < 30:
        return '18-29'
    elif A < 46:
        return '30-45'
    elif A < 66:
        return "46-65"
    else:
        return "66+"

def Gehaltsklassen(A):
    if A < 15000:
        return '15.000-'
    elif A < 30000:
        return '15.000-30.000'
    elif A < 50000:
        return "30.000-50.000"
    elif A < 70000:
        return "50.000-70.000"
    elif A < 90000:
        return "70.000-90.000"
    else:
        return "90.000+"
#endregion

#ytd = 2020
df_YTD = fetch_dataframe(ytd)

df_YTD['Altersklassen'] = df_YTD['Alter'].map(Altersklassen)
df_YTD['Gehaltsklassen'] = df_YTD['Gehalt'].map(Gehaltsklassen)

#Berechnug der Werte in den "Werte-Karten"
Gewinn_YTD = df_YTD["Gewinn"].sum()
Anzahl_YTD = df_YTD["Anzahl"].sum()
Prob_YTD=round(df_YTD["Anzahl"].sum()/df_YTD["Anzahl"].count(),2)*100

fig_kpis = fetch_kpi_indicator(Gewinn_YTD, Anzahl_YTD, Prob_YTD)

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

#Websiten-Aufbau
layout = html.Div(children=[
    #region Menüleiste
    dbc.Row([
        dbc.Col(
            html.Div(style={"margin-top": "20px", },  children = [
                html.H1(children="Kennziffern im aktuellen Jahr"),
                dcc.Tabs(id="tabs_kpi", value='Gewinn', children=[
                    dcc.Tab(label='Gewinn', value='Gewinn'),
                    dcc.Tab(label='Anzahl', value='Anzahl'),
                    dcc.Tab(label="Kaufwahrscheinlichkeit", value="Kaufbereitschaft")
                ])
            ]), width = 12
        ),
    ], justify = "center"),
    #endregion

    #region Chart-Reihe 1
    dbc.Row([
        dbc.Col(html.Div(id="Produktplot_1"), width = 7),
        dbc.Col(
            html.Div(style = {"background-color": "white", "margin-top": "20px"}, children=[
               dcc.Graph(figure = fig_kpis)
            ]), width = 4
        )
    ], justify="center", align="center", className="h-50"),
    #endregion
    
    #region Chart-Reihe 2
    dbc.Row([
        dbc.Col(
            html.Div(className = "box", style = {"height": "430px"}, children = [
                html.H5("Filter"),
                dcc.RadioItems(
                    id="radio_kpi",
                    options=[
                        {'label': 'Geschlecht', 'value': 'Geschlecht'},
                        {'label': 'Altersklassen', 'value': 'Altersklassen'},
                        {'label': 'Beruf', 'value': 'Job'},
                        {'label': 'Familienstand', 'value': 'Familienstand'},
                        {'label': 'Kinder', 'value': 'Kinder'},
                        {'label': 'Gehaltsklasse', 'value': 'Gehaltsklassen'}
                    ],
                    value='Geschlecht',
                    labelStyle={'display': 'block'}
                )
            ]), width = 2
        ),
        dbc.Col(html.Div(id="Produktplot_2"), width = 9)
    ], justify="center", align="center", className="h-50")
    #endregion
], style = CONTENT_STYLE)

@app.callback(Output(component_id = "Produktplot_1", component_property= 'children'),
              Input(component_id = 'tabs_kpi', component_property= 'value'))
def render_content(tab):
    if tab=="Kaufbereitschaft":
        temp_df = fetch_dataframe_prob(df_YTD, ["Angebotenes Produkt"])
        temp_fig = fetch_figure_bar(temp_df, "Angebotenes Produkt", "Kaufwahrscheinlichkeit in %", title="Kaufwahrscheinlichkeit[YTD] aufgeteilt nach Produkte")
        temp_fig.update_layout(height = 300)
        
        return html.Div(style={"margin-top": "20px"}, children = [
            dcc.Graph(figure=temp_fig )
        ])
    else:
        temp_df = fetch_dataframe_sum(df_YTD, ["Angebotenes Produkt"])
        temp_fig = fetch_figure_bar(temp_df, "Angebotenes Produkt", tab,  title = tab+ "[YTD] aufgeteilt nach Produkte" )  
        temp_fig.update_layout(height = 300)
        
        return html.Div(style={"margin-top": "20px"}, children = [
            dcc.Graph(figure = temp_fig)
        ])

    
@app.callback(Output("Produktplot_2", 'children'),
              Input('tabs_kpi', 'value'),
              Input("radio_kpi", 'value'))
def render_content(tab, radio):
    if tab=="Kaufbereitschaft":
        temp_df = fetch_dataframe_prob(df_YTD, [radio])
        temp_fig = fetch_figure_bar(temp_df ,radio, "Kaufwahrscheinlichkeit in %", title= "Kaufwahrscheinlichkeit[YTD] aufgeteilt nach "+radio)
        temp_fig.update_layout(height = 450)

        return html.Div(style={"margin-top": "20px"}, children = [
            dcc.Graph(figure = temp_fig)
        ])
    else:
        temp_df = fetch_dataframe_sum(df_YTD, ["Angebotenes Produkt", radio])
        temp_fig = fetch_figure_bar(temp_df, radio, tab, color = "Angebotenes Produkt",  title = tab + "[YTD] aufgeteilt nach " + radio )
        temp_fig.update_layout(height = 450)

        return html.Div(style={"margin-top": "20px"}, children = [
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

@cache.memoize()    
def fetch_figure_bar(dataframe, x, y, title, color = None, text = None):
    if color != None and text == None:
        return px.bar(dataframe, x=x, y=y, color=color, title=title)
    elif color == None and text == None:
        return px.bar(dataframe, x=x, y=y, title=title, height= 300)
    elif color == None and text != None:
        fig_temp = px.bar(dataframe, x=x, y=y, title=title, text=text)
        fig_temp.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig_temp.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    else:
        fig_temp = px.bar(dataframe, x=x, y=y, title=title, color=color, text=text)
        fig_temp.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig_temp.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        return fig_temp

@cache.memoize()
def fetch_dataframe_sum(dataframe, args):
    return dataframe.groupby(args).sum().reset_index()

def fetch_dataframe_prob(dataframe, args):
    temp_df = dataframe.groupby(args)["Anzahl"].apply(lambda x: round((x.sum()/x.count())*100, 2)).reset_index()
    df_renamed=temp_df.rename(columns={'Anzahl': 'Kaufwahrscheinlichkeit in %'})
    return df_renamed

