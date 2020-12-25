import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import dask.dataframe as dd

df = dd.read_sql_table("allgemeine_daten", 'Kundendaten.db', "index")

df['Monat'] = df['Monat'].apply(lambda x: str(x).zfill(2))
df["Datum"]=df["Jahr"].map(str)+"-"+df["Monat"].map(str)+"-"+df["Tag"].map(str)
pd.to_datetime(df["Datum"], format="%Y-%m-%d")
df["Monats-Datum"] = df['Datum'].astype(str).str[:7]
pd.to_datetime(df["Monats-Datum"], format="%Y-%m")
#df=pd.merge(df, df_Gewinne, left_on='Angebotenes Produkt', right_on='Bankprodukt')
#df.drop(columns=["Bankprodukt"])
df["Anzahl"]=np.where(df["Gekauft"]=="ja", 1,0)
#df["Gewinn pro Verkauf"]=np.where(df["Gekauft"]=="nein", 0, df["Gewinn pro Verkauf"])
df["Gewinn"]=df["Gewinn pro Verkauf"]

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


df_Gewinn_pro_Monat=df.groupby(["Monats-Datum", "Angebotenes Produkt"])["Gewinn"].sum().reset_index()
df_Anzahl_pro_Monat=df.groupby(["Monats-Datum", "Angebotenes Produkt"])["Anzahl"].sum().reset_index()

df_Gewinn_pro_Monat_Geschlecht=df.groupby(["Monats-Datum", "Geschlecht"])["Gewinn"].sum().reset_index()
df_Anzahl_pro_Monat_Geschlecht=df.groupby(["Monats-Datum", "Geschlecht"])["Anzahl"].sum().reset_index()
df_Gewinn_pro_Monat_Alter=df.groupby(["Monats-Datum", "Altersklassen"])["Gewinn"].sum().reset_index()
df_Anzahl_pro_Monat_Alter=df.groupby(["Monats-Datum", "Altersklassen"])["Anzahl"].sum().reset_index()
df_Gewinn_pro_Monat_Job=df.groupby(["Monats-Datum", "Job"])["Gewinn"].sum().reset_index()
df_Anzahl_pro_Monat_Job=df.groupby(["Monats-Datum", "Job"])["Anzahl"].sum().reset_index()
df_Gewinn_pro_Monat_Familie=df.groupby(["Monats-Datum", "Familienstand"])["Gewinn"].sum().reset_index()
df_Anzahl_pro_Monat_Familie=df.groupby(["Monats-Datum", "Familienstand"])["Anzahl"].sum().reset_index()
df_Gewinn_pro_Monat_Kinder=df.groupby(["Monats-Datum", "Kinder"])["Gewinn"].sum().reset_index()
df_Anzahl_pro_Monat_kinder=df.groupby(["Monats-Datum", "Kinder"])["Anzahl"].sum().reset_index()
df_Gewinn_pro_Monat_Gehalt=df.groupby(["Monats-Datum", "Gehaltsklassen"])["Gewinn"].sum().reset_index()
df_Anzahl_pro_Monat_Gehalt=df.groupby(["Monats-Datum", "Gehaltsklassen"])["Anzahl"].sum().reset_index()

fig1_Gewinn=px.line(df_Gewinn_pro_Monat, x="Monats-Datum", y="Gewinn", color="Angebotenes Produkt", title="Bankprodukte ~ Gewinn")
fig1_Anzahl=px.line(df_Anzahl_pro_Monat, x="Monats-Datum", y="Anzahl", color="Angebotenes Produkt", title="Bankprodukte ~ Anzahl")


fig2_Gewinn_Geschlecht=px.line(df_Gewinn_pro_Monat_Geschlecht, x="Monats-Datum", y="Gewinn", color="Geschlecht", title="Geschlecht ~ Gewinn")
fig2_Anzahl_Geschlecht=px.line(df_Anzahl_pro_Monat_Geschlecht, x="Monats-Datum", y="Anzahl", color="Geschlecht", title="Geschlecht ~ Anzahl")
fig2_Gewinn_Alter=px.line(df_Gewinn_pro_Monat_Alter, x="Monats-Datum", y="Gewinn", color="Altersklassen", title="Alter ~ Gewinn")
fig2_Anzahl_Alter=px.line(df_Anzahl_pro_Monat_Alter, x="Monats-Datum", y="Anzahl", color="Altersklassen", title="Alter ~ Anzahl")
fig2_Gewinn_Job=px.line(df_Gewinn_pro_Monat_Job, x="Monats-Datum", y="Gewinn", color="Job", title="Job ~ Gewinn")
fig2_Anzahl_Job=px.line(df_Anzahl_pro_Monat_Job, x="Monats-Datum", y="Anzahl", color="Job", title="Job ~ Anzahl")
fig2_Gewinn_Familie=px.line(df_Gewinn_pro_Monat_Familie, x="Monats-Datum", y="Gewinn", color="Familienstand", title="Familienstand ~ Gewinn")
fig2_Anzahl_Familie=px.line(df_Anzahl_pro_Monat_Familie, x="Monats-Datum", y="Anzahl", color="Familienstand", title="Familienstand ~ Anzahl")
fig2_Gewinn_Kinder=px.line(df_Gewinn_pro_Monat_Kinder, x="Monats-Datum", y="Gewinn", color="Kinder", title="Kinder ~ Gewinn")
fig2_Anzahl_Kinder=px.line(df_Anzahl_pro_Monat_kinder, x="Monats-Datum", y="Anzahl", color="Kinder", title="Kinder ~ Anzahl")
fig2_Gewinn_Gehalt=px.line(df_Gewinn_pro_Monat_Gehalt, x="Monats-Datum", y="Gewinn", color="Gehaltsklassen", title="Gehalt ~ Gewinn")
fig2_Anzahl_Gehalt=px.line(df_Anzahl_pro_Monat_Gehalt, x="Monats-Datum", y="Anzahl", color="Gehaltsklassen", title="Gehalt ~ Anzahl")

Gewinn_Vorjahr=round(df[df["Jahr"] == (df["Jahr"].max()-1)].Gewinn.sum(),2)
Gewinn_aktuell=round(df[df["Jahr"] == (df["Jahr"].max())].Gewinn.sum(),2)
Gewinn_Veränderung=round(Gewinn_aktuell-Gewinn_Vorjahr,2)
Anzahl_Vorjahr=round(df[df["Jahr"] == (df["Jahr"].max()-1)].Anzahl.sum(),2)
Anzahl_aktuell=round(df[df["Jahr"] == (df["Jahr"].max())].Anzahl.sum(),2)
Anzahl_Veränderung=round(Anzahl_aktuell-Anzahl_Vorjahr,2)

layout = html.Div([
    html.H1(children="KPI´s im Zeitverlauf"),
    dcc.Tabs(id="tabs", value='tabs_Gewinn', children=[
        dcc.Tab(label='Gewinn', value='tabs_Gewinn'),
        dcc.Tab(label='Anzahl', value='tabs_Anzahl'),
    ]),

    html.H2("Bankprodukte im Zeitverlauf"),
    html.Div(id="Zeitplot_1"),

    html.H2("KPI´s im Zeitverlauf"),
    html.Div(id="Zeit_Karte",children =[
        html.H3("            Vorjahr        aktuelles Jahr         Veränderung"),
        dcc.Markdown(f'''Gewinn     {Gewinn_Vorjahr}     {Gewinn_aktuell}   {Gewinn_Veränderung }'''),
        dcc.Markdown(f'''Anzahl      {Anzahl_Vorjahr}     {Anzahl_aktuell}   {Anzahl_Veränderung }''')
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
    html.Div(id="Zeitplot_2")
])

@app.callback(Output("Zeitplot_1", 'children'),
              Input('tabs', 'value'))

def render_content(tab):
    if tab == 'tabs_Gewinn':
        return html.Div([
            dcc.Graph(figure=fig1_Gewinn)
        ])
    elif tab == 'tabs_Anzahl':
        return html.Div([
            dcc.Graph(figure=fig1_Anzahl)
        ])

@app.callback(Output("Zeitplot_2", 'children'),
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