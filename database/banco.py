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
            data_coleta DATETIME DEFAULT CURRENT_TIMESTAMP
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

#def menores_precos():
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            nome,
            loja,
            link,
            MIN(preco)
        FROM produtos
        GROUP BY nome, loja
        ORDER BY MIN(preco)
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados

#def comparar_produto(termo):

    termo = normalizar_nome(termo)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            nome,
            loja,
            MIN(preco)
            FROM produtos
            WHERE nome_normalizado LIKE ?
            GROUP BY nome_normalizado, loja
            ORDER BY MIN(preco)
    """, (f"%{termo}%",))

    dados = cursor.fetchall()

    conn.close()

    return dados


#def comparar_normalizado(termo):
    
    conn = conectar()
    cursor = conn.cursor()

    termo = normalizar_nome(termo)

    cursor.execute("""
        SELECT
            nome_normalizado,
            loja,
            MIN(preco)
        FROM produtos
        WHERE nome_normalizado LIKE ?
        GROUP BY nome_normalizado, loja
        ORDER BY MIN(preco)
    """, (f"%{termo}%",))

    dados = cursor.fetchall()

    conn.close()

    return dados

#def ranking_precos(termo):

    conn = conectar()
    cursor = conn.cursor()

    termo = normalizar_nome(termo)

    cursor.execute("""
        SELECT
            nome_normalizado,
            loja,
            MIN(preco)
        FROM produtos
        WHERE nome_normalizado LIKE ?
        GROUP BY nome_normalizado, loja
        ORDER BY MIN(preco)
    """, (f"%{termo}%",))

    dados = cursor.fetchall()

    conn.close()

    return dados

def melhor_oferta(termo):

    conn = conectar()
    cursor = conn.cursor()

    termo = normalizar_nome(termo)

    cursor.execute("""
        SELECT
            codigo,
            nome,
            loja,
            MIN(preco) as preco,
            link
        FROM produtos
        WHERE nome_normalizado LIKE ?
        GROUP BY codigo
        ORDER BY preco ASC
    """, (f"%{termo}%",))

    resultado = cursor.fetchone()

    conn.close()

    return resultado

#def historico_precos(termo):

    conn = conectar()
    cursor = conn.cursor()

    termo = normalizar_nome(termo)

    cursor.execute("""
        SELECT
            data_coleta,
            loja,
            preco
        FROM produtos
        WHERE nome_normalizado LIKE ?
        ORDER BY data_coleta
    """, (f"%{termo}%",))

    dados = cursor.fetchall()

    conn.close()

    return dados

#def detectar_quedas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            nome_normalizado,
            loja,
            MIN(preco),
            MAX(preco)
        FROM produtos
        GROUP BY nome_normalizado, loja
        HAVING MIN(preco) < MAX(preco)
        ORDER BY
            (MAX(preco) - MIN(preco)) DESC
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados

#def buscar_por_codigo(codigo):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            nome,
            loja,
            preco,
            link
        FROM produtos
        WHERE codigo = ?
        ORDER BY preco
    """, (codigo,))

    dados = cursor.fetchall()

    conn.close()

    return dados

#def melhor_oferta_codigo(codigo):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            nome,
            loja,
            preco,
            link
        FROM produtos
        WHERE codigo = ?
        ORDER BY preco ASC
        LIMIT 1
    """, (codigo,))

    resultado = cursor.fetchone()

    conn.close()

    return resultado

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
        AND id = (
            SELECT MAX(id)
            FROM produtos
            WHERE codigo = p.codigo
            AND loja = p.loja
        )
    """, (f"%{termo}%",))

    dados = cursor.fetchall()

    conn.close()

    termos_busca = termo.split()

    resultado_filtrado = []

    for item in dados:

        nome = normalizar_nome(item[0])

        score = 0

        for palavra in termos_busca:

            if palavra in nome:
                score += 1

        resultado_filtrado.append(
            (score, item)
        )

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

    conn.close()

    return dados