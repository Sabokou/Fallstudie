import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
import plotly.graph_objects as go
import dask.dataframe as dd
import plotly.express as px

df = dd.read_sql_table("testdaten", 'sqlite:///Kundendaten.db', "index")
df=df.compute()
df_BCG_1= df.groupby(["Angebotenes Produkt"])[["Gewinn", "Anzahl"]].sum().reset_index()
df_BCG_2=df.groupby(["Angebotenes Produkt"])["Anzahl"].apply(lambda x: x.sum()/x.count())

df_BCG=df_BCG_1.merge(df_BCG_2, on="Angebotenes Produkt")
df_BCG=df_BCG.rename(columns={"Anzahl_x": "Anzahl", "Anzahl_y":"Kaufwahrscheinlichkeit"})
df_BCG["Kaufwahrscheinlichkeit in %"]=df_BCG["Kaufwahrscheinlichkeit"]*100
df_BCG["Gewinn pro Verkauf in €"]=df_BCG["Gewinn"]/df_BCG["Anzahl"]


fig = px.scatter(df_BCG, x=df_BCG["Kaufwahrscheinlichkeit in %"], y=df_BCG["Gewinn pro Verkauf in €"], color="Angebotenes Produkt")




fig.add_trace(go.Scatter(
    x=[12.5, 12.5],
    y=[4.5, 4.5],
    text=["<b>Poor Dogs</b>"],
    mode="text",showlegend = False
))
fig.add_trace(go.Scatter(
    x=[12.5, 12.5],
    y=[9.5, 9.5],
    text=["<b>Questionmarks</b>"],
    mode="text",showlegend = False
))
fig.add_trace(go.Scatter(
    x=[37.5, 37.5],
    y=[4.5, 4.5],
    text=["<b>Cash Cows</b>"],
    mode="text",showlegend = False
))
fig.add_trace(go.Scatter(
    x=[37.5, 37.5],
    y=[9.5, 9.5],
    text=["<b>Stars</b>"],
    mode="text",showlegend = False
))

fig.update_xaxes(range=[0, 50], showgrid=False)
fig.update_yaxes(range=[0, 10], showgrid=False)

fig.add_shape(type="rect",
    x0=0, y0=0, x1=25, y1=5,
    line=dict(color="RoyalBlue"),
)
fig.add_shape(type="rect",
    x0=25, y0=0, x1=50, y1=5,
    line=dict(color="RoyalBlue"),
)
fig.add_shape(type="rect",
    x0=0, y0=5, x1=25, y1=10,
    line=dict(color="RoyalBlue"),
)
fig.add_shape(type="rect",
    x0=25, y0=5, x1=50, y1=10,
    line=dict(color="RoyalBlue"),
)
        
fig.update_traces(marker=dict(size=20,line=dict(width=2)))
fig.update_layout(margin=dict(t=0), height=600, width=1100)

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

layout = html.Div(children = [
    dbc.Row([html.Div(style = {"margin-top":"15px"}, children = [html.H1(children=["BCG-Matrix nach Gewinn pro Verkauf und Kaufwahrscheinlichkeit"])])], justify = "center"),
    dbc.Row([html.Div(style = {"margin-top":"15px"}, children = [dcc.Graph(figure=fig)])], justify = "center")
], style = CONTENT_STYLE)