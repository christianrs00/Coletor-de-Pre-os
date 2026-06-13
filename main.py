from database.banco import *
from scrapers.mercadolivre import pesquisar

criar_tabelas()

produto = input("Produto: ")

resultados = pesquisar(produto)

for item in resultados:

    salvar_produtos(
        item["nome"],
        item["loja"],
        item["preco"],
        item["link"]
    )

print(
    f"{len(resultados)} Registros salvos!"
)