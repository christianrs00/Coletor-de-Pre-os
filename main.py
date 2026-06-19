from database.banco import criar_tabelas, salvar_produto

from scrapers.kabum import pesquisar as pesquisar_kabum
from scrapers.terabyte import pesquisar as pesquisar_terabyte


criar_tabelas()

produto = input("Digite o Produto: ")

print("\nPesquisar Kabum...")
resultados_kabum = pesquisar_kabum(produto)
print("Kabum:", len(resultados_kabum))

print("\nPesquisar Terabyte...")
resultados_terabyte = pesquisar_terabyte(produto)
print("Terabyte:", len(resultados_terabyte))

resultados = (
    resultados_kabum +
    resultados_terabyte
)

print(f"\nTotal: {len(resultados)}")

salvos = 0

for item in resultados:

    inserido = salvar_produto(
        item["nome"],
        item["loja"],
        item["preco"],
        item["link"]
    )

    if inserido:
        salvos += 1

print(f"{salvos} novos registros adicionados.")