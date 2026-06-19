import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from database.banco import menores_precos


dados = menores_precos()

print("\n===== MENORES PREÇOS =====")

for nome, codigo, loja, preco in dados:
    print(
        f"{loja: <12} | "
        f"R$ {preco:,.2f} | "
        f"{nome}"
    )