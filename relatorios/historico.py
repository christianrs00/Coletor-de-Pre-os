import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from database.banco import historico_precos

produto = input("Produto: ")

dados = historico_precos(produto)

print("\n===== HISTÓRICO DE PREÇOS =====\n")

for data, loja, preco in dados:

    print(
        f"{data} | "
        f"{loja:<10} | "
        f"R$ {preco:.2f}"
    )