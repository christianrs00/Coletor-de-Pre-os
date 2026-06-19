import re

def extrair_codigo(nome):

    nome = nome.upper()

    padroes = [

        r"\d+-\d+[A-Z]+",           # 100-100000457BOX

        r"[A-Z]{2}-[A-Z0-9-]+",     # CL-P137-AL12SW-A

        r"BX\d+",                   # BX80768285

        r"[A-Z]{4,}\d+[A-Z0-9]*",   # ACFRE00124A

        r"[A-Z]{2}\d{3,}",          # BK039
    ]

    for padrao in padroes:

        encontrado = re.search(
            padrao,
            nome
        )

        if encontrado:
            return encontrado.group(0)

    return None