import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('sqlite:///Kundendaten.db', execution_options={"sqlite_raw_colnames": True})
df = pd.read_sql("allgemeine_daten", con = engine)

print(df.head())
