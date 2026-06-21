from scrapers.kabum import pesquisar as pesquisar_kabum
from scrapers.terabyte import pesquisar as pesquisar_terabyte

from database.banco import salvar_produto
from database.banco import(salvar_produto, limpar_historico_antigo)
from database.banco import alertas_queda_preco

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

    limpar_historico_antigo(30)



    quedas = alertas_queda_preco()

    print("\n=== ALERTAS DE PREÇO ===")

    for item in quedas[:10]:

        economia = round(
            item[4] - item[3],
            2
        )

        print(
            f"{item[1]} | "
            f"{item[2]} | "
            f"↓ R$ {economia}"
        )