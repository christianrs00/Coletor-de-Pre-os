import sqlite3
import pandas as pd

conn = sqlite3.connect("produtos.db")

df = pd.read_sql_query(
    "SELECT * FROM precos",
    conn
)
df.to_excel(
    "promocoes.xlsx",
    index=False
)

conn.close()

print("Excel gerado! ")