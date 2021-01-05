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

ytd = 2020
df_YTD = fetch_dataframe(ytd)

#Mapping für Graphen-Gruppierungen
def Altersklassen(A):
    if A < 30:
        return 'Jung (18-29)'
    elif A < 46:
        return 'Junge Erwachsene (30-45)'
    elif A < 66:
        return "Alte Erwachsene (46-65)"
    else:
        return "Greise (66+)"

df_YTD['Altersklassen'] = df_YTD['Alter'].map(Altersklassen)

def Gehaltsklassen(A):
    if A < 15000:
        return 'Sehr niedrig (<15.000)'
    elif A < 30000:
        return 'niedrig (15.000-30.000)'
    elif A < 50000:
        return "Untere Mitte (30.000-50.000)"
    elif A < 80000:
        return "Obere Mitte (50.000-80.000)"
    elif A < 100000:
        return "Hoch (80.000-100.000)"
    else:
        return "Sehr hoch (>100.000)"

df_YTD['Gehaltsklassen'] = df_YTD['Gehalt'].map(Gehaltsklassen)

#Berechnug der Werte in den "Werte-Karten"
Gewinn_YTD = round(df_YTD["Gewinn"].sum(),2)
Anzahl_YTD = round(df_YTD["Anzahl"].sum(),2)
Prob_YTD=round(df_YTD["Anzahl"].sum()/df_YTD["Anzahl"].count(),2)

#Websiten-Aufbau
layout = html.Div(children=[
    #region Menüleiste
    dbc.Row([
        dbc.Col(
            html.Div(children = [
                html.H1(children="Kennziffern im aktuellen Jahr"),
                dcc.Tabs(id="tabs_kpi", value='Gewinn', children=[
                    dcc.Tab(label='Gewinn', value='Gewinn'),
                    dcc.Tab(label='Anzahl', value='Anzahl'),
                    dcc.Tab(label="Kaufbereitschaft", value="Kaufbereitschaft")
                ])
            ]), width = 12
        ),
    ]),
    #endregion
    #region Chart-Reihe 1
    dbc.Row([
        dbc.Col(html.Div(id="Produktplot_1"), width = 7),
        dbc.Col(
            html.Div(children=[
                html.Table(id="Wert-Karte", children=[
                    html.Thead(children=[
                        html.Tr(children = [
                            html.Th(""),
                            html.Th("Wert [YTD]")
                            ])
                    ]),
                    html.Tbody(children=[
                        html.Tr(children=[
                            html.Th("Gewinn"),
                            html.Td(Gewinn_YTD)
                        ]),
                        html.Tr(children=[
                            html.Th("Anzahl"),
                            html.Td(Anzahl_YTD)
                        ]),
                        html.Tr(children=[
                            html.Th("Wahrscheinlichkeit"),
                            html.Td(str(round(Prob_YTD*100,2)) + "%" )
                        ])
                    ])
                ])
            ]), width = 4
        )
    ], justify="center", align="center", className="h-50"),
    #endregion
    #region Chart-Reihe 2
    dbc.Row([
        dbc.Col(
            html.Div(children = [
                html.H4("Filter"),
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
            ]), width = 1
        ),
        dbc.Col(html.Div(id="Produktplot_2"), width = 8)
    ], justify="center", align="center", className="h-50")
    #endregion
])

@app.callback(Output(component_id = "Produktplot_1", component_property= 'children'),
              Input(component_id = 'tabs_kpi', component_property= 'value'))
def render_content(tab):
    if tab=="Kaufbereitschaft":
        temp_df = fetch_dataframe_prob(df_YTD, ["Angebotenes Produkt"])
        temp_fig = fetch_figure_bar(temp_df, "Angebotenes Produkt", "Anzahl", title="Kaufwahrscheinlichkeit in Prozent")
        
        return html.Div(className = "m_links", children = [
            dcc.Graph(figure=temp_fig )
        ])
    else:
        temp_df = fetch_dataframe_sum(df_YTD, ["Angebotenes Produkt"])
        temp_fig = fetch_figure_bar(temp_df, "Angebotenes Produkt", tab,  title = tab + " verkaufter Produkter [YTD]" )   
        
        return html.Div(className = "m_links", children = [
            dcc.Graph(figure = temp_fig, config = {'responsive': True})
        ])

    
@app.callback(Output("Produktplot_2", 'children'),
              Input('tabs_kpi', 'value'),
              Input("radio_kpi", 'value'))
def render_content(tab, radio):
    if tab=="Kaufbereitschaft":
        temp_df = fetch_dataframe_prob(df_YTD, [radio])
        temp_fig = fetch_figure_bar(temp_df ,radio, "Anzahl", title="Kaufwahrscheinlichkeit in Prozent")
        
        return html.Div(className = "u_rechts", children = [
            dcc.Graph(figure = temp_fig, config = {'responsive': True} )
        ])
    else:
        temp_df = fetch_dataframe_sum(df_YTD, ["Angebotenes Produkt", radio])
        temp_fig = fetch_figure_bar(temp_df, radio, tab, color = "Angebotenes Produkt",  title = tab + " verkaufter Produkte nach " + radio + " [YTD]" )
        temp_fig.update_layout(margin = {t:5, b:5, l:5, r:5})
        return html.Div(className = "u_rechts", children = [
            dcc.Graph(figure=temp_fig, config = {'responsive': True})
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
    return dataframe.groupby(args)["Anzahl"].apply(lambda x: round((x.sum()/x.count())*100, 2)).reset_index()
