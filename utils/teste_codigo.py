from codigo_produto import extrair_codigo
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from utils.codigo_produto import extrair_codigo

testes = [

    "Processador AMD Ryzen 5 5500, AM4, 100-100000457BOX",

    "Processador Intel Core Ultra 9 285, BX80768285",

    "Cooler Be Quiet Pure Rock 3, BK039",

    "Cooler Thermaltake Astria 200, CL-P137-AL12SW-A",

    "Cooler Arctic Freezer 36 ARGB, ACFRE00124A"

]

for item in testes:

    print(item)

    print(
        extrair_codigo(item)
    )

    print("-" * 50)