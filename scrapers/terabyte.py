import requests
import re

from bs4 import BeautifulSoup
from urllib.parse import quote


def pesquisar(produto):

    busca = quote(produto)

    url = f"https://www.terabyteshop.com.br/busca?str={busca}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        )
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        print("Status Terabyte:", response.status_code)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        cards = soup.find_all(
            "div",
            class_="product-item__box"
        )

        print("Cards encontrados:", len(cards))

        resultados = []

        for card in cards:

            try:

                link_tag = card.find(
                    "a",
                    class_="product-item__image"
                )

                if not link_tag:
                    continue

                nome = (
                    link_tag.get("title", "")
                    .strip()
                )

                link = (
                    link_tag.get("href", "")
                    .strip()
                )

                # Extrai o ID da URL
                match = re.search(
                    r"/produto/(\d+)/",
                    link
                )

                if match:
                    codigo = f"TERA-{match.group(1)}"
                else:
                    codigo = None

                preco_div = card.find(
                    "div",
                    class_="product-item__new-price"
                )

                if not preco_div:
                    continue

                preco_span = preco_div.find("span")

                if not preco_span:
                    continue

                preco_texto = (
                    preco_span.text
                    .replace("R$", "")
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
                )

                preco = float(preco_texto)

                print(nome)
                print(codigo)
                print("-" * 50)

                resultados.append({
                    "codigo": codigo,
                    "nome": nome,
                    "preco": preco,
                    "link": link,
                    "loja": "Terabyte"
                })

            except Exception as erro:
                print("Erro item:", erro)

        print("RESULTADOS:", len(resultados))

        return resultados

    except Exception as erro:
        print("Erro geral:", erro)
        return []