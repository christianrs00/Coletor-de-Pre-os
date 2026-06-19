from database.banco import menor_precos

import pandas as pd
import os

dados = menor_precos()

if not dados:
    print("Nenhum dado encontrado.")
    exit()

df = pd.DataFrame(
    dados,
    columns=[
        "Produto",
        "Loja",
        "Menor Preco"
    ]
)

os.makedirs("relatorios", exist_ok=True)

arquivo = "relatorios/menores_precos.xlsx"

df.to_excel(
    arquivo,
    index=False
)

print(f"Relatório gerado: {arquivo}")