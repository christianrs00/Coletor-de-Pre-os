import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)
from database.banco import ranking_precos

produto = input("Produto: ")

dados = ranking_precos(produto)

print("\n===== RANKING DE PREÇOS =====\n")

for nome, loja, preco in dados:

    print(f"{loja:<12} R$ {preco:>8.2f} | {nome}")