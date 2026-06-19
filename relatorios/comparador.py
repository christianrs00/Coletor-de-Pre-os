import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from database.banco import comparar_normalizado

produto = input("Produto: ")

dados = comparar_normalizado(produto)

print("\n===== COMPARADOR =====")

for nome, loja, preco, link in dados:

    print(nome)
    print(f" {loja} R$ {preco:.2f} | {link}")
    print("." * 80)