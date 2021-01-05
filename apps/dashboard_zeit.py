import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app, cache
import plotly.express as px
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

df = fetch_dataframe()

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
Gewinn_Veränderung=round((Gewinn_aktuell-Gewinn_Vorjahr)/Gewinn_Vorjahr,2)
Anzahl_Vorjahr=round(df_Vorjahr["Anzahl"].sum(),2)
Anzahl_aktuell=round(df_aktuell["Anzahl"].sum(),2)
Anzahl_Veränderung=round((Anzahl_aktuell-Anzahl_Vorjahr)/Anzahl_Vorjahr,2)
Prob_Vorjahr=round(df_Vorjahr["Anzahl"].sum()/df_Vorjahr["Anzahl"].count(),4)
Prob_aktuell=round(df_aktuell["Anzahl"].sum()/df_aktuell["Anzahl"].count(),4)
Prob_Veränderung=round(Prob_aktuell-Prob_Vorjahr,4)

layout = html.Div(children = [
        dbc.Row([
            dbc.Col(
                html.Div(children = [
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
            html.Div(style = {"vertical-align":"middle"}, children= [ 
                html.Table(id="Zeit-Karte", children=[
                    html.Thead(children=[
                        html.Tr(children = [
                            html.Th(""),
                            html.Th("Vorjahr"),
                            html.Th("Aktuelles Jahr [YTD]"),
                            html.Th("Veränderung")
                            ])
                    ]), 
                    html.Tbody(children=[
                        html.Tr(children=[
                            html.Th("Gewinn"),
                            html.Td(round(Gewinn_Vorjahr,2) ),
                            html.Td(round(Gewinn_aktuell,2) ),
                            html.Td(str(round(Gewinn_Veränderung,2))+"%" )
                        ]),
                        html.Tr(children=[
                            html.Th("Anzahl"),
                            html.Td(Anzahl_Vorjahr),
                            html.Td(Anzahl_aktuell),
                            html.Td(str(round(Anzahl_Veränderung,2)), "%")
                        ]),
                        html.Tr(children=[
                            html.Th("Wahrscheinlichkeit"),
                            html.Td(str(round(Prob_Vorjahr*100,2)) + "%"),
                            html.Td(str(round(Prob_aktuell*100,2)) + "%"),
                            html.Td(str(round(Prob_Veränderung*100,2)) + "%")
                        ])
                    ])
                ])
            ]), width = 5
        )
    ], justify="center", align="center", className="h-50"),

    dbc.Row([
        dbc.Col(
            html.Div(children=[
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
])

@app.callback(Output("Zeitplot_1", 'children'),
              Input('tabs_zeit', 'value'))
def render_content(tab):
    if tab=="Kaufbereitschaft":
        return html.Div(className = "m_links", children = [
            dcc.Graph(figure=fetch_figure_line(fetch_dataframe_prob(df, ["Datum","Angebotenes Produkt"]), \
                "Datum", "Kaufwahrscheinlichkeit in %", color="Angebotenes Produkt", title="Kaufwahrscheinlichkeit aufgeteilt nach Produkte") )
        ])
    else:    
        temp_dataframe = fetch_dataframe_sum(df, ["Datum", "Angebotenes Produkt"])
        temp_fig = fetch_figure_line(temp_dataframe,\
            "Datum", tab, color="Angebotenes Produkt",  title = tab+" aufgeteilt nach Produkte")
        
        return html.Div(className = "m_links", children = [
            dcc.Graph(figure= temp_fig)
        ])

@app.callback(Output("Zeitplot_2", 'children'),
               Input('tabs_zeit', 'value'),
               Input("radio_zeit", "value"))
def render_content(tab, radio):
    if tab=="Kaufbereitschaft":
        return html.Div(className = "m_links", children = [
            dcc.Graph(figure=fetch_figure_line(fetch_dataframe_prob(df, ["Datum",radio]), \
                "Datum", "Kaufwahrscheinlichkeit in %", color=radio, title="Kaufwahrscheinlichkeit aufgeteilt nach "+radio) )
        ])
    else:  
        temp_df = fetch_dataframe_sum(df, ["Datum", radio])
        temp_fig = fetch_figure_line(temp_df, "Datum", tab,\
             color = radio,  title = tab + " aufgeteilt nach " + radio)
    
        return html.Div(className = "m_links", children = [
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