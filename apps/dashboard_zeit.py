import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app, cache

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
from datetime import datetime
import dask.dataframe as dd
import dask.array as da


@cache.memoize()
def fetch_dataframe():
    df = dd.read_sql_table("testdaten", 'sqlite:///Kundendaten.db', "index")
    # df["Datum"] = df['Datum'].astype(str).str[:7]
    df.set_index(df.Datum)
    return df

@cache.memoize()
def fetch_kpi_card(df):

    df_Vorjahr=df[df["Jahr"] == (df["Jahr"].max()-1)].compute()
    df_aktuell=df[df["Jahr"] == (df["Jahr"].max())].compute()
    Gewinn_Vorjahr=round(df_Vorjahr["Gewinn"].sum(),2)
    Gewinn_aktuell=round(df_aktuell["Gewinn"].sum(),2)
    #Gewinn_Veränderung=round((Gewinn_aktuell-Gewinn_Vorjahr)/Gewinn_Vorjahr,2)
    Anzahl_Vorjahr=round(df_Vorjahr["Anzahl"].sum(),2)
    Anzahl_aktuell=round(df_aktuell["Anzahl"].sum(),2)
    #Anzahl_Veränderung=round((Anzahl_aktuell-Anzahl_Vorjahr)/Anzahl_Vorjahr,2)
    Prob_Vorjahr=round(df_Vorjahr["Anzahl"].sum()/df_Vorjahr["Anzahl"].count(),2)*100
    Prob_aktuell=round(df_aktuell["Anzahl"].sum()/df_aktuell["Anzahl"].count(),2)*100
    #Prob_Veränderung=round(Prob_aktuell-Prob_Vorjahr,4)

    fig = go.Figure()

    fig.update_layout(height = 450)

    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = Gewinn_aktuell,
        title = {"text": "Gewinn"},
        delta = {'reference': Gewinn_Vorjahr, 'relative': True, 'position' : "bottom"},
        number = {'suffix': "€"},
        domain = {'x': [0, 0.5], 'y': [0.7, 1]}))

    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = Anzahl_aktuell,
        title = {"text": "Anzahl"},
        delta = {'reference': Anzahl_Vorjahr, 'relative': True, 'position' : "bottom"},
        number = {'suffix': " "},
        domain = {'x': [0.5, 1], 'y': [0.7, 1]}))

    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = Prob_aktuell,
        title = {"text": "Kaufwahrscheinlichkeit"},
        delta = {'reference': Prob_Vorjahr, 'relative': True, 'position' : "bottom"},
        number = {'suffix': "%"},
        domain = {'x': [0.3, 0.7], 'y': [0, 0.3]}))

    return fig

#region Mapping der einzelnen Spalten
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

def Altersklassen(A):
    if A < 30:
        return '18-29'
    elif A <46:
        return '30-45'
    elif A<66:
        return "46-65"
    else:
        return "66+"
#endregion


df = fetch_dataframe()

df['Altersklassen'] = df['Alter'].map(Altersklassen)

df['Gehaltsklassen'] = df['Gehalt'].map(Gehaltsklassen)

kpi_indicator = fetch_kpi_card(df)

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

layout = html.Div(children = [
        dbc.Row([
            dbc.Col(
                html.Div(style = {"margin-top":"20px"}, children = [
                    html.H1(children="KPI´s im Zeitverlauf"),
                    dcc.Tabs(id="tabs_zeit", value='Gewinn', children=[
                        dcc.Tab(label='Gewinn', value='Gewinn'),
                        dcc.Tab(label='Anzahl', value='Anzahl'),
                        dcc.Tab(label="Kaufwahrscheinlichkeit", value="Kaufbereitschaft")
                    ])
                ]), width = 12
            ),
        ], justify="center"),

    #html.H2("Bankprodukte im Zeitverlauf"),
    dbc.Row([
        dbc.Col(html.Div(id="Zeitplot_1"), width = 7),
        dbc.Col(
            html.Div(style = {"margin-top":"20px","vertical-align":"middle"}, children= [ 
                dcc.Graph(figure = kpi_indicator)
            ]), width = 5
        )
    ], justify="center", align="center", className="h-50"),

    dbc.Row([
        dbc.Col(
            html.Div(className = "box", style = {"height": "450px", "margin-top":"20px"}, children=[
                html.H5("Filter"),
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
                    labelStyle={'display': 'block'}
                )
            ]), width = 2,
        ),
        dbc.Col(html.Div(id="Zeitplot_2"), width = 9)
    ], justify="center", align="center", className="h-50")
], style = CONTENT_STYLE)

@app.callback(Output("Zeitplot_1", 'children'),
              Input('tabs_zeit', 'value'))
def render_content(tab):
    if tab=="Kaufbereitschaft":
        return html.Div(style = {"margin-top":"20px"}, children = [
            dcc.Graph(figure=fetch_figure_line(fetch_dataframe_prob(df, ["Datum","Angebotenes Produkt"]), \
                "Datum", "Kaufwahrscheinlichkeit in %", color="Angebotenes Produkt", title="Kaufwahrscheinlichkeit aufgeteilt nach Produkte") )
        ])
    else:    
        temp_dataframe = fetch_dataframe_sum(df, ["Datum", "Angebotenes Produkt"])
        temp_fig = fetch_figure_line(temp_dataframe,\
            "Datum", tab, color="Angebotenes Produkt",  title = tab+" aufgeteilt nach Produkte")
        temp_fig.update_layout(height = 450)

        return html.Div(style = {"margin-top":"20px"}, children = [
            dcc.Graph(figure= temp_fig)
        ])

@app.callback(Output("Zeitplot_2", 'children'),
               Input('tabs_zeit', 'value'),
               Input("radio_zeit", "value"))
def render_content(tab, radio):
    if tab=="Kaufbereitschaft":
        return html.Div(style = {"margin-top":"20px"}, children = [
            dcc.Graph(figure=fetch_figure_line(fetch_dataframe_prob(df, ["Datum",radio]), \
                "Datum", "Kaufwahrscheinlichkeit in %", color=radio, title="Kaufwahrscheinlichkeit aufgeteilt nach "+radio) )
        ])
    else:  
        temp_df = fetch_dataframe_sum(df, ["Datum", radio])
        temp_fig = fetch_figure_line(temp_df, "Datum", tab,\
             color = radio,  title = tab + " aufgeteilt nach " + radio)
        temp_fig.update_layout(height = 450)

        return html.Div(style = {"margin-top":"20px"}, children = [
            dcc.Graph(figure=temp_fig)
        ])

@cache.memoize()
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
        fig_temp = px.bar(dataframe, x = x, y = y, title=title, color=color, text=text)
        fig_temp.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig_temp.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        return fig_temp

@cache.memoize()
def fetch_dataframe_sum(dataframe, args):
    return dataframe.groupby(args).sum().reset_index().compute()
    #return dataframe.groupby(args).sum().reset_index()
@cache.memoize()
def fetch_dataframe_prob(dataframe, args):
    temp_df = dataframe.groupby(args)["Anzahl"].apply(lambda x: round((x.sum()/x.count())*100, 2)).reset_index().compute()
    df_renamed=temp_df.rename(columns={'Anzahl': 'Kaufwahrscheinlichkeit in %'})
    return df_renamed


