# verificar_banco.py

import sqlite3

conn = sqlite3.connect("produtos.db")

cursor = conn.cursor()

cursor.execute("""
SELECT nome, preco, loja
FROM produtos
ORDER BY id DESC
LIMIT 10
""")

for linha in cursor.fetchall():
    print(linha)

conn.close()