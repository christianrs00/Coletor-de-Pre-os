import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from database.banco import detectar_quedas

dados = detectar_quedas()

print("\n===== QUEDAS DE PREÇO =====\n")

for nome, loja, menor, maior in dados:

    economia = maior - menor

    print(nome)
    print(
        f"{loja} | "
        f"De R$ {maior:.2f} "
        f"Para R$ {menor:.2f}"
    )
    print(
        f"Economia: R$ {economia:.2f}"
    )

    print("-" * 80)