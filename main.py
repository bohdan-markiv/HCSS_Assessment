from prepare_tables import prepare_full_tables
import pandas as pd

df = prepare_full_tables()
df.to_csv("data/prepared_tables.csv")
