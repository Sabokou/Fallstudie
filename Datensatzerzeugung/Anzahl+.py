import dask.dataframe as dd
import dask.array as da

df = dd.read_sql_table("allgemeine_daten", 'sqlite:///Kundendaten.db', "Jahr")
print("1. Schritt")
df["Anzahl"]= da.where(df['Gekauft'] == "ja", 1, 0).compute()
print("2. Schritt")
df.to_sql("allgemeine_daten", if_exists="replace")