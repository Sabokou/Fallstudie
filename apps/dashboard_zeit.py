import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import pandas as pd
import numpy as np

from sqlalchemy import create_engine
engine = create_engine('sqlite:///Kundendaten.db', execution_options={"sqlite_raw_colnames": True})
df = pd.read_sql("allgemeine_daten", con = engine)
df_Gewinne=pd.read_excel("Gewinne_pro_Produkt.xlsx", engine='openpyxl')

df['Monat'] = df['Monat'].apply(lambda x: str(x).zfill(2))
df["Datum"]=df["Jahr"].map(str)+"-"+df["Monat"].map(str)+"-"+df["Tag"].map(str)
pd.to_datetime(df["Datum"], format="%Y-%m-%d")
df["Monats-Datum"] = df['Datum'].astype(str).str[:7]
df=pd.merge(df, df_Gewinne, left_on='Angebotenes Produkt', right_on='Bankprodukt')
df.drop(columns=["Bankprodukt"])
df["Anzahl"]=np.where(df["Gekauft"]=="ja", 1,0)
df["Gewinn pro Verkauf"]=np.where(df["Gekauft"]=="nein", 0, df["Gewinn pro Verkauf"])



layout = html.Div([
    



])