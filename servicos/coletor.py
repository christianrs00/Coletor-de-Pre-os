from scrapers.kabum import pesquisar as pesquisar_kabum
from scrapers.terabyte import pesquisar as pesquisar_terabyte

from database.banco import salvar_produto


def atualizar_produto(produto):

    resultados = []

    resultados.extend(
        pesquisar_kabum(produto)
    )

    resultados.extend(
        pesquisar_terabyte(produto)
    )

    novos = 0

    for item in resultados:

        if salvar_produto(
            item["codigo"],
            item["nome"],
            item["loja"],
            item["preco"],
            item["link"]
        ):
            novos += 1

    print(f"Novos registros: {novos}")