import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from database.banco import melhor_oferta

produto = input("Produto: ")

resultado = melhor_oferta(produto)

print("\n===== MELHOR OFERTA =====\n")

if resultado:

    nome, loja, preco, link = resultado

    print("Produto:")
    print(nome)

    print("\nLoja:")
    print(loja)

    print("\nPreço:")
    print(f"R$ {preco:.2f}")

    print("\nLink:")
    print(link)

else:

    print("Nenhum produto encontrado.")