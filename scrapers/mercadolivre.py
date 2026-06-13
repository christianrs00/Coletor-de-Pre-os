from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import quote


def criar_driver():

    options = Options()

    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=options)


def pesquisar(produto):

    url = f"https://lista.mercadolivre.com.br/{quote(produto)}"

    driver = criar_driver()

    resultados = []

    try:

        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".ui-search-result")
            )
        )

        itens = driver.find_elements(
            By.CSS_SELECTOR,
            ".ui-search-result"
        )

        for item in itens[:10]:

            try:

                titulo = item.find_element(
                    By.CSS_SELECTOR,
                    ".poly-component__title"
                ).text

                preco = item.find_element(
                    By.CSS_SELECTOR,
                    ".andes-money-amount__fraction"
                ).text

                link = item.find_element(
                    By.TAG_NAME,
                    "a"
                ).get_attribute("href")

                preco = float(
                    preco.replace(".", "")
                )

                resultados.append({
                    "nome": titulo,
                    "preco": preco,
                    "link": link,
                    "loja": "Mercado Livre"
                })

            except Exception as erro_item:
                print("Erro no item:", erro_item)

    except Exception as erro:
        print("Erro geral:", erro)

    finally:
        driver.quit()

    return resultados