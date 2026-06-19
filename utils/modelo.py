import re

def extrair_modelo(texto):

    padroes = [
        r'ryzen\s+\d+\s+\d+[a-z0-9]*',
        r'rtx\s+\d+',
        r'rx\s+\d+',
        r'i[3579]-\d+[a-z]*'
    ]

    texto = texto.lower()

    for padrao in padroes:

        match = re.search(
            padrao,
            texto
        )

        if match:
            return match.group()

    return None