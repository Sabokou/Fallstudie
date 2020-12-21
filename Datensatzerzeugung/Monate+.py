import pandas as pd
from random import *

from sqlalchemy import create_engine
engine = create_engine('sqlite:///Kundendaten.db', execution_options={"sqlite_raw_colnames": True})
df = pd.read_sql("Kundendaten", con = engine)
df['Jahr'] = df.apply(lambda row: choice([2018, 2018, 2019, 2019, 2019, 2020]), axis=1)
df['Monat'] = df.apply(lambda row: choice(list(range(1,13))), axis=1)
df['Tag'] = df.apply(lambda row: choice(list(range(1,29))),axis=1) 

df.to_sql("Kundendaten", con=engine,if_exists="replace")
print("done")