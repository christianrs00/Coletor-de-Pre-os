import requests
import re
import json

def pesquisar(produto):

    url = f"https://www.kabum.com.br/busca/{produto.replace(' ', '-')}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )
    }

    resposta = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        resposta.text,
        re.DOTALL
    )

    if not match:
        print("NEXT_DATA não encontrado")
        return []

    dados = json.loads(match.group(1))

    produtos = (
        dados["props"]
        ["pageProps"]
        ["data"]
        ["catalogServer"]
        ["data"]
    )

    resultados = []

    for item in produtos:

        try:

            nome = item.get("name", "")

            preco = item.get(
                "priceWithDiscount",
                item.get("price", 0)
            )

            codigo_loja = item.get("code")

            if not codigo_loja:
                continue

            codigo = f"KABUM-{codigo_loja}"

            slug = item.get("friendlyName", "")

            link = (
                f"https://www.kabum.com.br/produto/"
                f"{codigo_loja}/{slug}"
            )

            print(nome)
            print(codigo)
            print("-" * 50)

            resultados.append({
                "codigo": codigo,
                "nome": nome,
                "preco": float(preco),
                "link": link,
                "loja": "Kabum"
            })

        except Exception as erro:
            print("Erro produto:", erro)

    return resultados