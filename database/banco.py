import sqlite3
from utils.normalizador import normalizar_nome
#from utils.codigo_produto import extrair_codigo
from pathlib import Path

DB = Path(__file__).parent / "produtos.db"

def conectar():
    return sqlite3.connect(DB)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT,
            nome TEXT,
            nome_normalizado TEXT,
            loja TEXT,
            preco REAL,
            link TEXT,
            data_coleta DATETIME DEFAULT CURRENT_TIMESTAMP,
            ultima_verificacao DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
     # Índice para busca por código
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_codigo
        ON produtos(codigo)
    """)

    # Índice para busca por nome normalizado
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_nome_normalizado
        ON produtos(nome_normalizado)
    """)

    # Índice para consultas por loja
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_loja
        ON produtos(loja)
    """)

    # Índice composto usado nas consultas mais frequentes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_codigo_loja
        ON produtos(codigo, loja)
    """)

    conn.commit()
    conn.close()

def salvar_produto(codigo, nome, loja, preco, link):
    conn = conectar()
    cursor = conn.cursor()

    nome_normalizado = normalizar_nome(nome)

    cursor.execute("""
        SELECT preco
        FROM produtos
        WHERE codigo = ?
        AND loja = ?
        ORDER BY id DESC
        LIMIT 1
                   
    """, (codigo, loja))

    ultimo_registro = cursor.fetchone()

    if ultimo_registro:
        ultimo_preco = ultimo_registro[0]

        if float(ultimo_preco) == float(preco):
            conn.close()
            return False
   
    cursor.execute("""
        INSERT INTO produtos
        (codigo, nome, nome_normalizado, loja, preco, link)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (codigo, nome, nome_normalizado, loja, preco, link))


    conn.commit()
    conn.close()

    return True

def buscar_produto_web(termo):

    conn = conectar()
    cursor = conn.cursor()

    termo = normalizar_nome(termo)

    cursor.execute("""
        SELECT
            nome,
            loja,
            preco,
            link
        FROM produtos p
        WHERE nome_normalizado LIKE ?
        AND datetime(data_coleta) >= datetime('now', '-3 days')
        AND id = (
            SELECT MAX(id)
            FROM produtos
            WHERE codigo = p.codigo
            AND loja = p.loja
        )
        LIMIT 300
    """, (f"%{termo}%",))

    dados = cursor.fetchall()

    conn.close()

    termos_busca = termo.split()

    resultado_filtrado = []

    for item in dados:

        nome = normalizar_nome(item[0])

        # Ignorar somente kits
        if "kit upgrade" in nome:
            continue

        score = 0

        for palavra in termos_busca:
            if palavra in nome:
                score += 1

        # Exige todas as palavras pesquisadas
        if score < len(termos_busca):
            continue

        resultado_filtrado.append(
            (score, item)
        )

    print("\nSCORES:")
    for score, item in resultado_filtrado:
        print(score, item[2], item[0][:80])

    resultado_filtrado.sort(
        key=lambda x: (-x[0], x[1][2])
    )

    vistos = set()
    resultado_final = []

    for score, item in resultado_filtrado:

        chave = (
            item[0].lower().strip(),
            item[1]
        )

        if chave in vistos:
            continue

        vistos.add(chave)
        resultado_final.append(item)

    print("\nRESULTADOS FINAIS:")
    for r in resultado_final:
        print(r)

    return resultado_final

def historico_grafico(termo):

    conn = conectar()
    cursor = conn.cursor()

    termo = normalizar_nome(termo)

    cursor.execute("""
        SELECT
            DATE(data_coleta),
            MIN(preco)
        FROM produtos
        WHERE nome_normalizado LIKE ?
        GROUP BY DATE(data_coleta)
        ORDER BY DATE(data_coleta)
    """, (f"%{termo}%",))

    dados = cursor.fetchall()

    conn.close()

    return dados

def melhores_ofertas_loja(termo):

    conn = conectar()
    cursor = conn.cursor()

    termo = normalizar_nome(termo)

    cursor.execute("""
        SELECT
            loja,
            MIN(preco)
        FROM produtos p
        WHERE nome_normalizado LIKE ?
        AND id = (
            SELECT MAX(id)
            FROM produtos
            WHERE codigo = p.codigo
            AND loja = p.loja
        )
        GROUP BY loja
        ORDER BY MIN(preco)
    """, (f"%{termo}%",))


    dados = cursor.fetchall()

    print(dados)

    conn.close()

    return dados

def limpar_historico_antigo(dias=30):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM produtos
        WHERE data_coleta < datetime(
            'now',
            ?
        )
    """, (f"-{dias} days",))

    removidos = cursor.rowcount

    conn.commit()
    conn.close()

    print(f"Registros removidos: {removidos}")

    return removidos

def verificar_queda_preco(codigo, loja):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT preco
        FROM produtos
        WHERE codigo = ?
        AND loja = ?
        ORDER BY id DESC
        LIMIT 2
    """, (codigo, loja))

    dados = cursor.fetchall()

    conn.close()

    if len(dados) < 2:
        return None

    preco_atual = dados[0][0]
    preco_anterior = dados[1][0]

    if preco_atual < preco_anterior:

        return {
            "queda": round(
                preco_anterior - preco_atual,
                2
            ),
            "anterior": preco_anterior,
            "atual": preco_atual
        }

    return None

def alertas_queda_preco():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT
            codigo,
            loja
        FROM produtos
    """)

    produtos = cursor.fetchall()

    alertas = []

    for codigo, loja in produtos:

        cursor.execute("""
            SELECT
                nome,
                preco
            FROM produtos
            WHERE codigo = ?
            AND loja = ?
            ORDER BY id DESC
            LIMIT 2
        """, (codigo, loja))

        dados = cursor.fetchall()

        if len(dados) < 2:
            continue

        nome = dados[0][0]

        preco_atual = float(dados[0][1])
        preco_anterior = float(dados[1][1])

        if preco_atual < preco_anterior:

            valor_queda = round(
                preco_anterior - preco_atual,
                2
            )

            alertas.append(
                (
                    codigo,
                    nome,
                    loja,
                    preco_atual,
                    preco_anterior,
                    valor_queda
                )
            )

    conn.close()

    alertas.sort(
        key=lambda x: x[5],
        reverse=True
    )

    return alertas