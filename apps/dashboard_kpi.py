#Import Dash Componenets
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

import pandas as pd
import dask.dataframe as dd

import numpy as np

import plotly.express as px

from datetime import datetime
ytd = datetime.now().year

#Programmlogik
# currentYear = dt.datetime.now().year
# df_jahr = df.where("Jahr" == str(currentYear))
df = dd.read_sql_table("allgemeine_daten", 'sqlite:///Kundendaten.db', "Jahr")

df_YTD = df.loc[ytd].compute()
df_YTD["Anzahl"] = np.where(df_YTD["Gekauft"]=="ja", 1,0)
df_YTD.head()

Gewinn_YTD = df_YTD["Gewinn"].sum()
Anzahl_YTD = df_YTD["Anzahl"].sum()

#Websiten-Aufbau
layout = html.Div([
    html.H1(children="KPI´s im Zeitverlauf"),
    dcc.Tabs(id="tabs", value='tabs_Gewinn', children=[
        dcc.Tab(label='Gewinn', value='tabs_Gewinn'),
        dcc.Tab(label='Anzahl', value='tabs_Anzahl'),
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
    id="Radio2",
    options=[
        {'label': 'Geschlecht', 'value': 'Geschlecht'},
        {'label': 'Altersklassen', 'value': 'Alter'},
        {'label': 'Beruf', 'value': 'Job'},
        {'label': 'Familienstand', 'value': 'Familie'},
        {'label': 'Kinder', 'value': 'Kinder'},
        {'label': 'Gehaltsklasse', 'value': 'Gehalt'}
    ],
    value='Geschlecht',
    labelStyle={'display': 'inline-block'}
    ), 
    html.Div(id="Produktplot_2")
])

@app.callback(Output(component_id = "Produktplot_1", component_property= 'children'),
              Input(component_id = 'tabs', component_property= 'value'))
def render_content(tab):
    if tab == 'tabs_Gewinn':
        return html.Div([
            dcc.Graph(figure=fetch_figure_bar(fetch_dataframe_sum(df_YTD, "Gewinn", ["Angebotenes Produkt"]),\
            "Angebotenes Produkt", "Gewinn",  title = "Gewinn pro Produkt [YTD]" ))
        ])
    elif tab == 'tabs_Anzahl':
        return html.Div([
            dcc.Graph(figure=fetch_figure_bar(fetch_dataframe_sum(df_YTD, "Anzahl", ["Angebotenes Produkt"]),\
            "Angebotenes Produkt", "Anzahl", title = "Anzahl verkaufter Produkte [YTD]" ))
        ])

    
@app.callback(Output("Produktplot_2", 'children'),
              Input('tabs', 'value'),
              Input("Radio2", "value"))
def render_content(tab, radio):
    if tab == 'tabs_Gewinn' and radio == "Geschlecht":
        return html.Div([
            dcc.Graph(figure=fig2_Gewinn_Geschlecht)
        ])
    elif tab == 'tabs_Anzahl' and radio == "Geschlecht":
        return html.Div([
            dcc.Graph(figure=fig2_Anzahl_Geschlecht)
        ])
    elif tab == 'tabs_Gewinn' and radio == "Alter":
        return html.Div([
            dcc.Graph(figure=fig2_Gewinn_Alter)
        ])
    elif tab == 'tabs_Anzahl' and radio == "Alter":
        return html.Div([
            dcc.Graph(figure=fig2_Anzahl_Alter)
        ])
    elif tab == 'tabs_Gewinn' and radio == "Job":
        return html.Div([
            dcc.Graph(figure=fig2_Gewinn_Job)
        ])
    elif tab == 'tabs_Anzahl' and radio == "Job":
        return html.Div([
            dcc.Graph(figure=fig2_Anzahl_Job)
        ])
    elif tab == 'tabs_Gewinn' and radio == "Familie":
        return html.Div([
            dcc.Graph(figure=fig2_Gewinn_Familie)
        ])
    elif tab == 'tabs_Anzahl' and radio == "Familie":
        return html.Div([
            dcc.Graph(figure=fig2_Anzahl_Familie)
        ])
    elif tab == 'tabs_Gewinn' and radio == "Kinder":
        return html.Div([
            dcc.Graph(figure=fig2_Gewinn_Kinder)
        ])
    elif tab == 'tabs_Anzahl' and radio == "Kinder":
        return html.Div([
            dcc.Graph(figure=fig2_Anzahl_Kinder)
        ])
    elif tab == 'tabs_Gewinn' and radio == "Gehalt":
        return html.Div([
            dcc.Graph(figure=fig2_Gewinn_Gehalt)
        ])
    elif tab == 'tabs_Anzahl' and radio == "Gehalt":
        return html.Div([
            dcc.Graph(figure=fig2_Anzahl_Gehalt)
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
    return dataframe.groupby(args).sum().reset_index()

def fetch_dataframe_count(dataframe, groupDirection, args):
    return dataframe.groupby(args).count().reset_index()
