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
df_BCG["Rentabilität"]=df_BCG["Gewinn"]/df_BCG["Anzahl"]

prob_max=df_BCG["Kaufwahrscheinlichkeit"].max()
rent_max=df_BCG["Rentabilität"].max()

fig = px.scatter(df_BCG, x=df_BCG["Kaufwahrscheinlichkeit"]/(prob_max+0.01), y=df_BCG["Rentabilität"]/(rent_max+0.1), color="Angebotenes Produkt",
                labels={
                     "x": "Skalierte Kaufwahrscheinlichkeit",
                     "y": "Skalierte Rentabilität",
                     "Angebotenes Produkt":"Angebotenes Produkt"
                 },)




fig.add_trace(go.Scatter(
    x=[0.25, 0.25],
    y=[0.45, 0.45],
    text=["Poor Dogs"],
    mode="text",showlegend = False
))
fig.add_trace(go.Scatter(
    x=[0.25, 0.25],
    y=[0.96, 0.96],
    text=["Questionmarks"],
    mode="text",showlegend = False
))
fig.add_trace(go.Scatter(
    x=[0.75, 0.75],
    y=[0.45, 0.45],
    text=["Cash Cows"],
    mode="text",showlegend = False
))
fig.add_trace(go.Scatter(
    x=[0.75, 0.75],
    y=[0.96, 0.96],
    text=["Stars"],
    mode="text",showlegend = False
))

fig.update_xaxes(range=[-0.01, 1.01], showgrid=False)
fig.update_yaxes(range=[-0.01, 1.01], showgrid=False)

fig.add_shape(type="rect",
    x0=-0.01, y0=-0.01, x1=0.5, y1=0.5,
    line=dict(color="RoyalBlue"),
)
fig.add_shape(type="rect",
    x0=0.5, y0=-0.01, x1=1.01, y1=0.5,
    line=dict(color="RoyalBlue"),
)
fig.add_shape(type="rect",
    x0=-0.01, y0=0.5, x1=0.5, y1=1.01,
    line=dict(color="RoyalBlue"),
)
fig.add_shape(type="rect",
    x0=0.5, y0=0.5, x1=1.01, y1=1.01,
    line=dict(color="RoyalBlue"),
)
        
fig.update_traces(marker=dict(size=20,line=dict(width=2)))
fig.update_layout(margin=dict(t=0), height=600, width=1100)



layout = html.Div(children = [
    dbc.Row([html.H1(children=["BCG-Matrix nach Rentabilität und Kaufwahrscheinlichkeit"])], justify = "center"),
    dbc.Row([dcc.Graph(figure=fig)], justify = "center")
])