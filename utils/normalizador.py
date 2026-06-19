import re

def normalizar_nome(nome):

    nome = nome.lower()

    remover = [
        "processador",
        "amd",
        "intel",
        "ghz",
        "max turbo",
        "sem vídeo",
        "sem video",
        "hexa core",
        "hexa-core",
        "threads",
        "Thread",
        "cooler",
        "wraith stealth"
        "am4",
        ",",
        "-",
        "(",
        ")"
    ]

    for termo in remover:
        nome = nome.replace(termo, " ")

    nome = re.sub(r"\d+\.\d+", " ", nome)

    nome = re.sub(r"\s+", " ", nome)

    return nome.strip()