import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import dask.dataframe as dd
import dask.array as da

"""
# Hallo Alina, ich hab die alle notwendigen Funktionen vollständig implementiert
# Es gibt 2 große TODO: 
# 1. Performance fixen für die Berechnung der "Karten"-Werte
# 2. Evtl. mal schauen, ob man die Performance der Graphen-Generation verbessern kann durch
# eine Neu-Indizierung nach "Monats-Datum", weil Operationen auf Index sind schneller :)
# VG Phillip
"""

df = dd.read_sql_table("testdaten", 'sqlite:///Kundendaten.db', "index")
df["Monats-Datum"] = df['Datum'].astype(str).str[:7]


def Altersklassen(A):
    if A < 30:
        return 'Jung (18-29)'
    elif A <46:
        return 'Junge Erwachsene (30-45)'
    elif A<66:
        return "Alte Erwachsene (46-65)"
    else:
        return "Greise (66+)"

df['Altersklassen'] = df['Alter'].map(Altersklassen)

def Gehaltsklassen(A):
    if A < 15000:
        return 'Sehr niedrig (<15.000)'
    elif A <30000:
        return 'niedrig (15.000-30.000)'
    elif A<50000:
        return "Untere Mitte (30.000-50.000)"
    elif A<80000:
        return "Obere Mitte (50.000-80.000)"
    elif A<100000:
        return "Hoch (80.000-100.000)"
    else:
        return "Sehr hoch (>100.000)"

df['Gehaltsklassen'] = df['Gehalt'].map(Gehaltsklassen)

#TODO: Überlegen ob das nicht performanter geht, weil es lange initiale  Ladezeiten produziert
df_Vorjahr=df[df["Jahr"] == (df["Jahr"].max()-1)].compute()
df_aktuell=df[df["Jahr"] == (df["Jahr"].max())].compute()
Gewinn_Vorjahr=round(df_Vorjahr["Gewinn"].sum(),2)
Gewinn_aktuell=round(df_aktuell["Gewinn"].sum(),2)
Gewinn_Veränderung=round(Gewinn_aktuell-Gewinn_Vorjahr,2)
Anzahl_Vorjahr=round(df_Vorjahr["Anzahl"].sum(),2)
Anzahl_aktuell=round(df_aktuell["Anzahl"].sum(),2)
Anzahl_Veränderung=round(Anzahl_aktuell-Anzahl_Vorjahr,2)

layout = html.Div([
    html.H1(children="KPI´s im Zeitverlauf"),
    dcc.Tabs(id="tabs_zeit", value='Gewinn', children=[
        dcc.Tab(label='Gewinn', value='Gewinn'),
        dcc.Tab(label='Anzahl', value='Anzahl'),
    ]),

    html.H2("Bankprodukte im Zeitverlauf"),
    html.Div(id="Zeitplot_1"),

    html.H2("KPI's im Zeitverlauf"),
    html.Div(id="Zeit_Karte",children =[
        html.H3("            Vorjahr        aktuelles Jahr         Veränderung"),
        dcc.Markdown(f'''Gewinn     {Gewinn_Vorjahr}     {Gewinn_aktuell}   {Gewinn_Veränderung }'''),
        dcc.Markdown(f'''Anzahl      {Anzahl_Vorjahr}     {Anzahl_aktuell}   {Anzahl_Veränderung }''')
        ]),


    html.H2("Features im Zeitverlauf"),
    dcc.RadioItems(
    id="radio_zeit",
    options=[
        {'label': 'Geschlecht', 'value': 'Geschlecht'},
        {'label': 'Altersklassen', 'value': 'Altersklassen'},
        {'label': 'Beruf', 'value': 'Job'},
        {'label': 'Familienstand', 'value': 'Familienstand'},
        {'label': 'Kinder', 'value': 'Kinder'},
        {'label': 'Gehaltsklasse', 'value': 'Gehaltsklassen'}
    ],
    value='Geschlecht',
    labelStyle={'display': 'inline-block'}
    ) , 
    html.Div(id="Zeitplot_2")
])

@app.callback(Output("Zeitplot_1", 'children'),
              Input('tabs_zeit', 'value'))
def render_content(tab):
        temp_dataframe = fetch_dataframe_sum(df, ["Monats-Datum", "Angebotenes Produkt"])
        temp_fig = fetch_figure_line(temp_dataframe,\
            "Monats-Datum", tab, color="Angebotenes Produkt",  title = "Bankprodukte ~ " + tab)
        
        return html.Div([
            
            dcc.Graph(figure= temp_fig)
        ])

@app.callback(Output("Zeitplot_2", 'children'),
               Input('tabs_zeit', 'value'),
               Input("radio_zeit", "value"))
def render_content(tab, radio):
    temp_df = fetch_dataframe_sum(df, ["Monats-Datum", radio])
    temp_fig = fetch_figure_line(temp_df, "Monats-Datum", tab,\
             color = radio,  title = tab + " ~ " + radio)
    
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

def fetch_dataframe_sum(dataframe, args):
    return dataframe.groupby(args).sum().reset_index().compute()
    #return dataframe.groupby(args).sum().reset_index()
